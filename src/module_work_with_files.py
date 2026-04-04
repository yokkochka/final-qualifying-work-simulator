from src.module_logger import CSVLogger
import src.module_custom_funcs as mcf 
import time
import os

logger = CSVLogger()


def open_file(path_to_file="", program =""):
    logger.info(f"файл module_work_with_files.py: Открытие файла {path_to_file}")

    mcf.win_m()
    
    # Вызываем окно "Выполнить"
    mcf.hotkey('win', 'r');
    mcf.human_delay() 
    
    mcf.type_text(f"{program} {path_to_file}")
    mcf.press_key('enter')
    mcf.human_delay()

    if os.path.exists(path_to_file):
        time.sleep(2)
        logger.info(f"файл module_work_with_files.py: Файл {path_to_file} успешно открыт")
        return True
    else:
        logger.error(f"файл module_work_with_files.py: Ошибка при открытии файла {path_to_file} - файл не найден")
        mcf.human_delay()
        mcf.press_key('enter')
        mcf.human_delay() 
        mcf.press_key('escape')
        return False

    


def create_text_file(path_to_file):
    logger.info(f"файл module_work_with_files.py: Создание текстового файла {path_to_file}")

    mcf.win_m()
    flag = 0
    if os.path.exists(path_to_file):
        flag = 1
    
    # Вызываем окно "Выполнить"
    mcf.hotkey('win', 'r');
    mcf.human_delay() 
    
    mcf.type_text(f"notepad")
    mcf.press_key('enter')
    mcf.human_delay()

    mcf.hotkey('ctrl', 'shift', 's')
    mcf.human_delay()

    mcf.type_text(path_to_file)
    mcf.human_delay()
    mcf.press_key('enter')
    mcf.human_delay()

    if flag == 1:
        mcf.press_key('left')
        mcf.human_delay()
        mcf.press_key('enter')

    mcf.human_delay()


    mcf.alt_f4()

    return

def open_notepad_and_write(text="Тестовая запись", path_to_txt=""):
    logger.info(f"файл module_work_with_files.py: Открытие Блокнота через Win+R")

    mcf.win_m()

    if os.path.exists(path_to_txt)== False:
        create_text_file(path_to_txt)

    if not open_file(path_to_txt, "notepad"):
        return
    
    # Пишем текст
    logger.info(f"файл module_work_with_files.py: Печать текста {text} в блокноте...")
    mcf.type_text(text)
    mcf.human_delay()

    
    # Сохраняем (Ctrl+S)
    mcf.ctrl_s()
    mcf.human_delay()
    

    # Закрываем
    mcf.alt_f4()
    logger.info(f"файл module_work_with_files.py: Блокнот закрыт")

    return