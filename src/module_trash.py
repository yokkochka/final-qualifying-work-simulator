import src.module_custom_funcs as mcf 
from src.module_logger import CSVLogger
import time
import winshell

logger = CSVLogger()

def is_trash_empty():
    return len(list(winshell.recycle_bin())) == 0

def clear_trash_bin():
    mcf.win_m()
    logger.info(f"файл module_trash.py: Очистка корзины")

    # Свернулся на рабочий стол 
    # mcf.win_d()

    # Открываем корзину
    mcf.move_to(20, 20, 0.5) # Верхний левый ярлычок на рабочем столе - корзина
    mcf.click(20,20,3)

    mcf.ctrl_a()
    mcf.human_delay()
    mcf.press_key('del')
    mcf.human_delay()
    mcf.press_key('enter')

    start_time = time.time()

    while is_trash_empty() == False and start_time - time.time() < 10:
        mcf.human_delay()

    mcf.human_delay()
    mcf.alt_f4()

  
    return