import src.module_custom_funcs as mcf 
from src.module_logger import CSVLogger
import time
import winshell

logger = CSVLogger()

def is_trash_empty():
    return len(list(winshell.recycle_bin())) == 0

def clear_trash_bin():
    mcf.win_m()
    logger.info(f"Начинается очистка корзины")

    logger.info(f"Открытие корзины")
    mcf.move_to(20, 20, 0.5) # 
    mcf.click(20,20,3)

    logger.info(f"Удаление содержимого корзины")
    mcf.ctrl_a()
    mcf.human_delay()
    mcf.press_key('del')
    mcf.human_delay()
    mcf.press_key('enter')

    start_time = time.time()

    logger.info(f"Ожидание завершения очистки корзины")
    while is_trash_empty() == False and start_time - time.time() < 10:
        mcf.human_delay()

    logger.info(f"Очистка корзины завершена")
    mcf.human_delay()
    mcf.alt_f4()

    return