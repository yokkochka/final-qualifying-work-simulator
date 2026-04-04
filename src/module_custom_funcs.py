import pyautogui as pg
import random
import time
from src.module_logger import CSVLogger

logger = CSVLogger()

def human_delay(min_sec=0.1, max_sec=0.5):
    # Внутренняя функция для создания небольших пауз.
    time.sleep(random.uniform(min_sec, max_sec))

# def move_to(x, y, duration=None):
#     if duration is None:
#         duration = random.uniform(0.5, 1.2)
#     try:
#         logger.info(f"файл module_custom_funcs.py: Перемещение мыши в ({x}, {y})", f"duration={duration}")
#         pg.moveTo(x, y, duration=duration, tween=pg.easeInOutQuad)
#     except Exception as e:
#         logger.info(f"файл module_custom_funcs.py: Ошибка при перемещении мыши {e}")

def move_to(x, y, duration=None):
    if duration is None:
        duration = random.uniform(0.5, 1.2)
    try:
        logger.info(f"файл module_custom_funcs.py: Перемещение мыши в ({x}, {y}), duration={duration:.2f}")
        pg.moveTo(x, y, duration=duration, tween=pg.easeInOutQuad)
    except Exception as e:
        logger.info(f"файл module_custom_funcs.py: Ошибка при перемещении мыши {e}")


def click(x=None, y=None, clicks=1, button='left'):
    try:
        ctx = f"coords=({x},{y}), clicks={clicks}, button={button}"
        logger.info(f"файл module_custom_funcs.py: Клик мышью {ctx}")
        pg.click(x=x, y=y, clicks=clicks, interval=random.uniform(0.1, 0.3), button=button)
        human_delay()
    except Exception as e:
        logger.info(f"файл module_custom_funcs.py: Ошибка при клике {e}")

def type_text(text, interval=None):
    if interval is None:
        interval = random.uniform(0.2, 0.4)
    try:
        logger.info(f"файл module_custom_funcs.py: Ввод текста (длина: {len(text)} симв.)")
        # pg.typewrite(text, interval=interval)
        pg.write(text, interval=interval)
        human_delay()
    except Exception as e:
        logger.info(f"файл module_custom_funcs.py: Ошибка при вводе текста {e}")

def press_key(key, presses=1):
    try:
        logger.info(f"файл module_custom_funcs.py: Нажатие клавиши: {key} Кол-во: {presses}")
        pg.press(key, presses=presses, interval=random.uniform(0.3, 0.5))
        human_delay()
    except Exception as e:
        logger.info(f"файл module_custom_funcs.py: Ошибка при нажатии {key} {str(e)}")

def hotkey(*args):
    try:
        logger.info(f"файл module_custom_funcs.py: Комбинация клавиш {('+'.join(args))}")
        pg.hotkey(*args)
        human_delay()
    except Exception as e:
        logger.info(f"файл module_custom_funcs.py: Ошибка комбинации {args} {str(e)}")

def alt_tab(count = 1):
    pg.keyDown('alt')
    for _ in range(count):
        pg.press('tab')
        time.sleep(0.2)
    pg.keyUp('alt')

def win_up():
    hotkey('win', 'up')

def win_d():
    hotkey('win', 'd')
    
def win_w():
    hotkey('win', 'w')

def ctrl_a():
    hotkey('ctrl', 'a')

def ctrl_s():
    hotkey('ctrl', 's')

def alt_f4():
    hotkey('alt', 'f4')

def win_m():
    hotkey('win', 'm')

def win_r_run(command):
    hotkey('win', 'r')
    time.sleep(0.5)
    type_text(command)
    press_key('enter')
    logger.info(f"файл module_custom_funcs.py: Запуск команды через Win+R Команда: {command}")

def sleep(seconds):
    logger.info(f"файл module_custom_funcs.py: Ожидание (Idle) {seconds} сек.")
    time.sleep(seconds)