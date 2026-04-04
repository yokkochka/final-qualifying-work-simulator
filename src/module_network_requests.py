import src.module_custom_funcs as mcf
from src.module_logger import CSVLogger
import pygetwindow as gw
import win32gui

logger = CSVLogger()

def watch_video(url,duration):

    if check_active_window_is_browser():
        mcf.hotkey('ctrl', 't')
    else:
        mcf.win_m()
        mcf.hotkey('win', 's')
        mcf.human_delay()

        mcf.type_text("Google Chrome")
        mcf.human_delay()
        mcf.press_key('enter')
        mcf.human_delay()
        mcf.hotkey('ctrl', 't')
        mcf.human_delay()

    mcf.type_text(url)
    mcf.human_delay()
    mcf.press_key('enter')
    mcf.human_delay()


    logger.info(f"файл module_network_requets: Начинается просмотр видео в течение {duration - 10} секунд...")
    mcf.sleep(duration - 10)
    logger.info(f"файл module_network_requets: Просмотр окончен")
    mcf.hotkey('alt', 'f4')


def check_active_window_is_browser():

    active_window = gw.getActiveWindow()
    
    if active_window and "Chrome" in active_window.title:
        return True
    for hwnd, title in get_all_windows():
        if "Chrome" in title:
            active_window = gw.getActiveWindow()
            count = 1
            while active_window and "Chrome" not in active_window.title:
                mcf.alt_tab(count)
                count += 1
                active_window = gw.getActiveWindow()
            mcf.human_delay()
            return True
    return False

def get_all_windows():
    windows = []

    def callback(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        windows.append((hwnd, title))

    win32gui.EnumWindows(callback, None)
    return windows


def open_url_in_browser(url):
    
    if check_active_window_is_browser():
        mcf.hotkey('ctrl', 't')
    else:
        mcf.win_m()
        mcf.hotkey('win', 's')
        mcf.human_delay()

        mcf.type_text("Google Chrome")
        mcf.human_delay()
        mcf.press_key('enter')
        mcf.human_delay()
        mcf.hotkey('ctrl', 't')
        mcf.human_delay()

    mcf.type_text(url)
    mcf.human_delay()
    mcf.press_key('enter')
    mcf.human_delay()


def download_file(url):
    if check_active_window_is_browser():
        mcf.hotkey('ctrl', 't')
    else:
        mcf.win_m()
        mcf.hotkey('win', 's')
        mcf.human_delay()

        mcf.type_text("Google Chrome")
        mcf.human_delay()
        mcf.press_key('enter')
        mcf.human_delay()
        mcf.hotkey('ctrl', 't')
        mcf.human_delay()

    mcf.type_text(url)
    mcf.human_delay()
    mcf.press_key('enter')
    mcf.human_delay()






