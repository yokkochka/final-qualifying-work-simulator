# Симулятор пользовательской активности (Windows)

Проект запускает сценарий пользовательских действий по расписанию из CSV-файла.
Подходит для имитации работы за ПК: открытие сайтов, скачивание файлов, взаимодействие с окнами, работа с файлами, очистка корзины.

## Возможности

- Выполнение задач по времени (`hour`, `minute`, `second`)
- Поддержка действий:
	- `watch_video`
	- `open_url`
	- `download_file`
	- `open_file`
	- `create_text_file`
	- `open_notepad_and_write`
	- `clear_trash`
	- `inaction`
- Логирование действий в `activity_log.csv`
- Проверка последовательности задач перед выполнением

## Требования

- ОС: **Windows**
- Браузер Google Chrome
- Масштаб экрана 100%
- Python: **3.11+** (рекомендуется)

## Установка

1. Создайте и активируйте виртуальное окружение:

```powershell
python -m venv venv
venv\Scripts\activate
```

2. Установите зависимости:

```powershell
pip install -r requirements.txt
```

Если при запуске есть ошибки импортов `pygetwindow` или `win32gui`, установите дополнительно:

```powershell
pip install PyGetWindow pywin32
```

## Сборка в exe (находясь в директории проекта)

Сначала установите Nuitka в активированное окружение:

```powershell
pip install nuitka
```

После этого можно собрать standalone-версию:

```powershell
python -m nuitka --follow-imports --standalone --jobs=4 --onefile --disable-console --include-package-data=flet main.py
```

После сборки для запуска достаточно иметь:

- файл `main.exe`
- рядом с ним файл `current_plan.csv`

Файл `activity_log.csv` будет создаваться автоматически при запуске.

## Структура проекта

- `main.py` - точка входа, чтение и выполнение плана
- `current_plan.csv` - активный план задач
- `actions.csv` - пример/шаблон набора задач
- `activity_log.csv` - лог действий
- `src/module_custom_funcs.py` - обертки над клавиатурой/мышью
- `src/module_network_requests.py` - работа с браузером
- `src/module_work_with_files.py` - операции с файлами/блокнотом
- `src/module_trash.py` - очистка корзины
- `src/module_logger.py` - CSV-логгер

## Формат плана (`current_plan.csv`)

Первая строка - заголовок:

```csv
hour,minute,second,action,params,duration
```

Описание полей:

- `hour`, `minute`, `second` - время запуска задачи
- `action` - имя действия
- `params` - строковый параметр действия (URL, путь, параметры)
- `duration` - минимальное время выполнения задачи в секундах

Пример:

```csv
hour,minute,second,action,params,duration
12,02,00,watch_video,https://rutube.ru/video/...,30
12,02,45,open_file,"C:\Users\User\Desktop\test.txt",20
12,03,30,open_notepad_and_write,"text=hello;path=C:\Users\User\Desktop\test.txt",20
12,04,20,clear_trash,"",10
```

## Поддерживаемые действия

Значения `duration` ниже указаны в точности как в `current_plan.csv` и считаются минимальным временем на выполнение.

- `watch_video`:
	- `params`: URL
	- `duration`: `30` 
- `open_url`:
	- `params`: URL
	- `duration`: `10` 
- `download_file`:
	- `params`: URL файла
	- `duration`: `20` 
- `open_file`:
	- `params`: путь к файлу
	- `duration`: `20` 
- `create_text_file`: 
	- `params`: путь к `.txt`
	- `duration`: `20` 
- `open_notepad_and_write`:
	- `params`: `text=<текст>;path=<путь>`
	- `duration`: `20` 
- `clear_trash`:
    - `params`: -
	- `duration`: `10` 
- `inaction`:
	- `duration`: сколько угодно

## Запуск

```powershell
python main.py
```

Перед запуском:

- Убедитесь, что `current_plan.csv` заполнен корректно и лежит рядом с main.py
- Желательно закрыть лишние окна и не использовать ПК во время выполнения сценария

## Логирование

Все действия пишутся в `activity_log.csv` в формате:

`timestamp;level;message;context`

## Важные замечания

- Проект управляет мышью и клавиатурой через GUI-автоматизацию.
- Координаты и поведение могут зависеть от разрешения экрана и расположения элементов.
- Часть сценариев ориентирована на Google Chrome.

