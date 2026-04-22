import csv
import random
import sys
import time
from datetime import datetime
from src.module_logger import CSVLogger
import src.module_custom_funcs as mcf
import src.module_trash as mt
import src.module_work_with_files as mwf
import src.module_network_requests as mnr
from datetime import datetime, timedelta

CSV_PATH = "current_plan.csv"
DELTA_BETWEEN_TASKS = 2  
logger = CSVLogger()

def start_execution():
    tasks = []
    
    try:
        with open(CSV_PATH) as f:
            reader = csv.DictReader(f)
            for row in reader:
                tasks.append(row)

        logger.info(f"CSV файл прочитан успешно. Всего строк найдено: {len(tasks)}")
    except Exception as e:
        logger.error(f"файл main.py: Ошибка при чтении CSV: {str(e)}")
        return []

    tasks.sort(key=lambda x: [int(x['hour']), int(x['minute']), int(x['second'])])
    logger.info(f"Найдено задач: {len(tasks)}")

    return tasks


def check_csv(tasks):
    """
    Проверяет CSV на корректность:
    - каждая задача начинается не раньше окончания предыдущей (учитывается duration)
    """
    if not tasks:
        return False

    previous_end_time = None

    for i, task in enumerate(tasks):
        try:
            start_time = datetime.strptime(f"{task['hour']}:{task['minute']}:{task['second']}", "%H:%M:%S")
            duration = int(task.get('duration', 0))
            end_time = start_time + timedelta(seconds=duration)
        except Exception as e:
            logger.error(f"файл main.py: Ошибка при парсинге времени/длительности в строке {i+1}: {e}")
            return False

        if previous_end_time and start_time < previous_end_time:
            logger.error(f"файл main.py: Нарушение последовательности: задача {i+1} ({task['action']}) " + \
                         f"начинается {start_time.time()}, но предыдущая задача заканчивается {previous_end_time.time()}")
            return False

        previous_end_time = end_time

    logger.info("CSV прошёл проверку на корректность последовательности задач по времени")
    return True



def main():
    global CSV_PATH
    flag_real_time = 1 
    
    logger.info("Приложение запущено")
    
    if len(sys.argv) == 1:
        logger.info("Аргументы не переданы, используется значение по умолчанию: план - current_plan.csv, выполнение - в реальном времени")
    elif len(sys.argv) == 2:
        if sys.argv[1].isdigit() and (sys.argv[1] == '0' or sys.argv[1] == '1'):
            flag_real_time = int(sys.argv[1])
            logger.info(f"Был передан только один аругумент для режима реального времени: {flag_real_time} (1 - в реальном времени, 0 - без учета реального времени)")
        elif sys.argv[1].endswith('.csv'):
            CSV_PATH = sys.argv[1]
            logger.info(f"Был передан только один аргумент, он распознан как путь к CSV файлу: {CSV_PATH}")
        else:
            logger.error(f"файл main.py: Был передан только один аргумент, но он не распознан ни как флаг реального времени, ни как путь к CSV файлу. Используются значения по умолчанию: план - current_plan.csv, выполнение - в реальном времени")
    elif len(sys.argv) == 3:
        if sys.argv[1].isdigit() and (sys.argv[1] == '0' or sys.argv[1] == '1'):
            flag_real_time = int(sys.argv[1])
            logger.info(f"Был передан корректный первый аругумент для режима реального времени: {flag_real_time} (1 - в реальном времени, 0 - без учета реального времени)")
        else:
            logger.error(f"файл main.py: Было передано два аргумента, но первый не распознан как флаг реального времени. Используется значение по умолчанию: выполнение - в реальном времени")
        if sys.argv[2].endswith('.csv'):
            CSV_PATH = sys.argv[2]
            logger.info(f"Был передан второй аргумент, он распознан как путь к CSV файлу: {CSV_PATH}")
        else:
            logger.error(f"файл main.py: Было передано два аргумента, но второй не распознан как путь к CSV файлу. Используются значения по умолчанию: план - current_plan.csv")
    else:
        logger.error(f"файл main.py: Ошибка в передаче аргументов, используются значения по умолчанию: план - current_plan.csv, выполнение - в реальном времени")
    
    mcf.win_m()
    tasks = start_execution()

    if check_csv(tasks) == False:
        logger.error("файл main.py: Ошибка валидации CSV (или он пустой). Исполнение прервано.")
        return  

    for task in tasks:
        task_time = datetime.strptime( f"{task['hour']}:{task['minute']}:{task['second']}", "%H:%M:%S")
        if flag_real_time == 1:
            delta = (datetime.now() - task_time).total_seconds()
            if delta > DELTA_BETWEEN_TASKS:
                logger.info(f"Пропуск задачи, т.к. прошло более" + \
                            f"{DELTA_BETWEEN_TASKS}-х секунд ({datetime.now()}) с предполагаемого времени исполнения: {task_time.time()}")
                continue
            else:
                logger.info(f"Задача будет выполнена с опозданием в {delta:.2f} секунд")
        
        while datetime.now() < task_time:
            time.sleep(1)
        
        logger.info(f"Начинается выполнение задачи {task['action']}" + \
                    f"({task['hour']}:{task['minute']}:{task['second']}) {task['params']} в {datetime.now().strftime('%H-%M-%S')}...")

        try:
            mcf.win_m()
            if task['action'] == 'test':
                for _ in range(int(task['duration'])):
                    mcf.move_to(random.randint(100, 500), random.randint(100, 500), 0.5)
            if task['action'] == 'inaction':
                time.sleep(int(task['duration']))
            elif task['action'] == 'clear_trash':
                mt.clear_trash_bin()
            elif task['action'] == 'open_file':
                mwf.open_file(path_to_file=task['params'])
            elif task['action'] == 'create_text_file':
                mwf.create_text_file(path_to_file=task['params'])
            elif task['action'] == 'open_notepad_and_write':
                text = task['params'].split(';')[0].split('=')[1] if 'text=' in task['params'] else "Text not provided"
                path = task['params'].split(';')[1].split('=')[1] if 'path=' in task['params'] else ""

                mwf.open_notepad_and_write(text=text, path_to_txt=path)
            elif task['action'] == "watch_video":
                mnr.watch_video(task['params'], int(task['duration']))
            elif task['action'] == "open_url":
                mnr.open_url_in_browser(task['params'])
            elif task['action'] == 'download_file':
                mnr.open_url_in_browser(task['params'])


        except Exception as e:
            logger.error(f"файл main.py: Ошибка при выполнении задачи: {str(e)}")
         

if __name__ == "__main__":
    main()