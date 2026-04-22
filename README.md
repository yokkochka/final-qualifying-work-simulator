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
- CSV-логирование (`INFO`, `DEBUG`, `ERROR`)

## Требования

- ОС: **Windows**
- Браузер Google Chrome
- Масштаб экрана 100%
- Python: **3.11+** (рекомендуется)

## Создание виртуального окружения

1. Создайте и активируйте виртуальное окружение (в директории проекта):

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


Собрать проект standalone-версию можно, используя следующую команду (при сборке везде выбрать `yes`):

```powershell
python -m nuitka --follow-imports --standalone --jobs=4 --onefile --disable-console --include-package-data=flet main.py
```

После сборки для запуска достаточно иметь:

- файл `main.exe`
- рядом с ним файл `current_plan.csv`

## Структура проекта


```text
final-qualifying-work-simulator/
├─ main.py
├─ current_plan.csv
├─ logs_dir/
│  └─ log_YYYY-MM-DD_HH-MM-SS.csv
├─ src/
│  ├─ module_custom_funcs.py
│  ├─ module_logger.py
│  ├─ module_network_requests.py
│  ├─ module_trash.py
│  └─ module_work_with_files.py
└─ README.md
```

- `main.py` - точка входа, чтение и выполнение плана
- `current_plan.csv` - активный план задач
- `logs_dir/` - директория с логами действий (при отсутствии создастся программно)
- `src/module_custom_funcs.py` - обертки над клавиатурой/мышью
- `src/module_network_requests.py` - работа с браузером
- `src/module_work_with_files.py` - операции с файлами/блокнотом
- `src/module_trash.py` - действия с корзиной
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


### Базовый запуск
Перед запуском:

- Убедитесь, что `current_plan.csv` заполнен корректно и лежит рядом с main.py
- Желательно закрыть лишние окна и не использовать ПК во время выполнения сценария

```powershell
python main.exe
```

Поведение по умолчанию:
- план: `current_plan.csv`
- режим выполнения: `real_time = 1` (с учетом текущего времени)


### Запуск с аргументами

Программа поддерживает аргументы командной строки:

1. Только флаг режима реального времени:
```powershell
python main.py 0
python main.py 1
```
- `1` — выполнение с учетом текущего времени
- `0` — выполнение без учета реального времени

2. Только путь к CSV:
```powershell
python main.py my_plan.csv
```

3. Флаг + путь к CSV:
```powershell
python main.py 0 my_plan.csv
python main.py 1 my_plan.csv
```

Если аргументы переданы некорректно, используются значения по умолчанию, а в лог пишется ошибка.


## Логирование

Логи создаются автоматически при каждом запуске:

- папка: `logs_dir/`
- имя файла: `log_YYYY-MM-DD_HH-MM-SS.csv`

Формат записей:
- `timestamp;level;message`
- в сообщении дополнительно может присутствовать контекст (по умолчанию `None`)

Уровни:
- `INFO`
- `DEBUG`
- `ERROR`

## Важные замечания

- Проект управляет мышью и клавиатурой через GUI-автоматизацию
- Координаты и поведение могут зависеть от разрешения экрана и расположения элементов
- Часть сценариев ориентирована на Google Chrome

