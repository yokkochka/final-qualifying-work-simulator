from src.module_logger import CSVLogger
import src.module_custom_funcs as mcf 
import time
import os

logger = CSVLogger()


def open_file(path_to_file="", program =""):
    logger.info(f"Открытие файла {path_to_file}")

    mcf.win_m()
    
    logger.info(f"Открытие файла {path_to_file} через Win+R")
    mcf.hotkey('win', 'r');
    mcf.human_delay() 
    
    logger.info(f"Ввод '{path_to_file}' для открытия файла")
    mcf.type_text(f"{program} {path_to_file}")
    mcf.press_key('enter')
    mcf.human_delay()


    if os.path.exists(path_to_file):
        time.sleep(2)
        logger.info(f"Файл {path_to_file} успешно открыт")
        return True
    else:
        logger.error(f"файл module_work_with_files.py: Ошибка при открытии файла {path_to_file} - файл не найден")
        mcf.human_delay()
        mcf.press_key('enter')
        mcf.human_delay() 
        mcf.press_key('escape')
        return False


def create_text_file(path_to_file):
    logger.info(f"Создание текстового файла {path_to_file}")

    mcf.win_m()
    flag = 0
    if os.path.exists(path_to_file):
        flag = 1
    
    logger.info(f"Открытие Блокнота через Win+R для создания файла {path_to_file}")
    mcf.hotkey('win', 'r');
    mcf.human_delay() 
    
    mcf.type_text(f"notepad")
    mcf.press_key('enter')
    mcf.human_delay()

    logger.info(f"Сохранение файла {path_to_file} через Ctrl+Shift+S")
    mcf.hotkey('ctrl', 'shift', 's')
    mcf.human_delay()

    logger.info(f"Ввод '{path_to_file}' для сохранения файла")
    mcf.type_text(path_to_file)
    mcf.human_delay()
    mcf.press_key('enter')
    mcf.human_delay()

    if flag == 1:
        logger.info(f"Файл {path_to_file} уже существует, сохранение перезаписало его")
        mcf.press_key('left')
        mcf.human_delay()
        mcf.press_key('enter')

    logger.info(f"Создание файла {path_to_file} завершено")
    mcf.human_delay()
    mcf.alt_f4()

    return

def open_notepad_and_write(text="Тестовая запись", path_to_txt=""):
    logger.info(f"Открытие Блокнота через Win+R")
    mcf.win_m()

    if os.path.exists(path_to_txt)== False:
        logger.info(f"Файл {path_to_txt} не найден, будет создан новый файл")
        create_text_file(path_to_txt)

    if not open_file(path_to_txt, "notepad"):
        logger.error(f"файл module_work_with_files.py: Не удалось открыть файл {path_to_txt} для записи текста")
        return
    
    logger.info(f"Печать текста {text} в блокноте")
    mcf.type_text(text)
    mcf.human_delay()

    logger.info(f"Сохранение текста в файл {path_to_txt}")
    mcf.ctrl_s()
    mcf.human_delay()
    
    mcf.alt_f4()
    logger.info(f"Блокнот закрыт")

    return