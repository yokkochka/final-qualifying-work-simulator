import csv
import random
import time
from datetime import datetime
from src.module_logger import CSVLogger
import src.module_custom_funcs as mcf
import src.module_trash as mt
import src.module_work_with_files as mwf
import src.module_network_requests as mnr
from datetime import datetime, timedelta


# CSV_PATH = "plan1.csv"
CSV_PATH = "current_plan.csv"

logger = CSVLogger()

def start_execution():
    tasks = []
    
    try:
        with open(CSV_PATH) as f:
            reader = csv.DictReader(f)
            print(reader)
            for row in reader:
                
                tasks.append(row)
        logger.info(f"файл main.py: CSV файл прочитан успешно. Всего строк найдено: {len(tasks)}")
    except Exception as e:
        logger.error(f"файл main.py: Ошибка при чтении CSV: {str(e)}")
        return []

    # сортируем по секундам (ВАЖНО)
    tasks.sort(key=lambda x: [int(x['hour']), int(x['minute']), int(x['second'])])

    # print(f"Найдено задач: {len(tasks)}")
    logger.info(f"файл main.py: Найдено задач: {len(tasks)}")
    print(tasks)
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

    logger.info("файл main.py: CSV прошёл проверку на последовательность задач")
    return True



def main():
    mcf.win_m()
    logger.info("файл main.py: Приложение запущено")

    # тут еще нужно поставить проверку корректности CSV 
    # (каждая задача занимает определенное минимальное кол-во секунд, 
    # нужнно смотреть что duration его не превышало)

    tasks = start_execution()

    if check_csv(tasks) == False:
        logger.error("файл main.py: Ошибка валидации CSV (или он пустой). Исполнение прервано.")
        return  

    for task in tasks:
        task_time = datetime.strptime( f"{task['hour']}:{task['minute']}:{task['second']}", "%H:%M:%S")

        # delta = (datetime.now() - task_time).total_seconds()
        # if delta > 2:
        #     logger.info(f"файл main.py: Пропуск задачи, т.к. прошло более" + \
        #                 f"2-х секунд ({datetime.now()}) с предполагаемого времени исполнения: {task_time.time()}")
        #     continue
        # else:
        #     logger.info(f"файл main.py: Задача будет выполнена с опозданием в {delta:.2f} секунд")
        
        while datetime.now() < task_time:
            time.sleep(1)
        
        logger.info(f"файл main.py: Выполнение задачи {task['action']}" + \
                    f"({task['hour']}:{task['minute']}:{task['second']}) {task['action']} в {datetime.now().time()}")

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
                # print(f"DEBUG: text={text}, path={path}")

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