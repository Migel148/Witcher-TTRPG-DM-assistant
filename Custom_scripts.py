import json
import operator
from RestrictedPython import compile_restricted
import PySimpleGUI as sg
import os
import datetime

def log(message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"

    try:
        with open("app_log.txt", "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        # print(f"Ошибка записи в лог: {e}")
        pass

def load_lists_json(filename,create_vars=True):
    """Загрузить все данные"""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # print(f"Данные загружены из {filename}")
        if create_vars:
            import inspect
            caller_globals = inspect.currentframe().f_back.f_globals
            for key, value in data.items():
                caller_globals[key] = value
                # print(f"  → {key} ({type(value).__name__} {len(value)})")

        return data

    else:
        # print(f"Файл {filename} не найден")
        return {}


def save_exec(code):
    print(code)
    byte_code = compile_restricted(code, filename='<inline>', mode='exec')
    # Передаём ограниченные встроенные функции и создаём пространство для переменных
    safe_globals = {
        "__builtins__": {
            "print": print,
            "range": range,
            "len": len,
            "__import__": __import__,  # Разрешаем импорт
            "open": open,  # Разрешаем работу с файлами
            "round": round,  # Разрешаем работу с файлами
            "str": str,  # Преобразование в строку
            "getitem": operator.getitem,
            "_getitem_": operator.getitem,
            "getattr": getattr,  # Добавляем getattr
            "_getattr_": getattr,
            "min": min,
            "max": max,
            "list": list,
            # Добавьте другие необходимые встроенные функции
        }
    }
    exec(byte_code, safe_globals)


def load_enemy_from_json(json_file_path):
    """
    Загружает данные о враге из JSON-файла.
    Возвращает кортеж из 12 элементов, совместимый с battle_layout_maker.
    """
    if not os.path.exists(json_file_path):
        # Пробуем найти .py файл как запасной вариант (для обратной совместимости)
        py_file_path = json_file_path.replace('.json', '.py')
        if os.path.exists(py_file_path):
            # Загружаем через старый метод (exec)
            return load_enemy_from_py(py_file_path)
        else:
            raise FileNotFoundError(f"Файл врага не найден: {json_file_path}")

    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Преобразуем данные в формат, ожидаемый battle_layout_maker
    # Конвертируем armor в список если это строка или число
    armor = data.get('armor', [])
    if isinstance(armor, str) or isinstance(armor, int):
        armor = [armor]

    # Получаем оружие (может называться weapon или weapons)
    weapons = data.get('weapon', data.get('weapons', []))

    # Извлекаем все данные
    return (
        data.get('stats', {}),
        data.get('added_stats', {}),
        data.get('skills', {}),
        armor,
        data.get('name', ''),
        weapons,
        data.get('mining', []),
        data.get('abilities', []),
        data.get('weakness', []),
        data.get('description', []),
        data.get('difficult', []),
        data.get('type', '')
    )


def load_enemy_from_py(py_file_path):
    """
    Загружает данные из Python-файла (для обратной совместимости)
    """
    import sys
    from RestrictedPython import compile_restricted
    import operator

    with open(py_file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    byte_code = compile_restricted(code, filename='<inline>', mode='exec')
    safe_globals = {
        "__builtins__": {
            "print": print,
            "range": range,
            "len": len,
            "__import__": __import__,
            "open": open,
            "round": round,
            "str": str,
            "getitem": operator.getitem,
            "_getitem_": operator.getitem,
            "getattr": getattr,
            "_getattr_": getattr,
            "min": min,
            "max": max,
            "list": list,
            "int": int,
            "float": float
        }
    }
    exec(byte_code, safe_globals)

    # Извлекаем переменные из safe_globals
    return (
        safe_globals.get('stats', {}),
        safe_globals.get('added_stats', {}),
        safe_globals.get('skills', {}),
        safe_globals.get('armor', []),
        safe_globals.get('name', ''),
        safe_globals.get('weapon', []),
        safe_globals.get('mining', []),
        safe_globals.get('abilities', []),
        safe_globals.get('weakness', []),
        safe_globals.get('description', []),
        safe_globals.get('difficult', []),
        safe_globals.get('type', '')
    )


def format_text(input_data, max_length=34):
    """Функция для обработки текста:
    - Если передан список, обрабатывает каждую строку в списке.
    - Если передана строка, обрабатывает её как одну строку."""

    def wrap_text(text, max_length):
        """Функция для переноса строки, если она длиннее max_length."""
        words = text.split()
        lines, current_line = [], []
        for word in words:
            # Проверяем длину текущей строки + слово
            if len(' '.join(current_line + [word])) > max_length:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                current_line.append(word)
        # Добавляем оставшиеся слова
        if current_line:
            lines.append(' '.join(current_line))
        return '\n'.join(lines)

    # Если входные данные — список
    if isinstance(input_data, list):
        return '\n'.join([wrap_text(line, max_length) for line in input_data])
    # Если входные данные — строка
    elif isinstance(input_data, str):
        return wrap_text(input_data, max_length)
    else:
        return "Unsupported data type!"


def get_file_tree_data(parent, directory, project_directory):
    files_folders = os.listdir(directory)
    for item in files_folders:
        full_path = f"{directory}/{item}"
        if os.path.isdir(full_path):
            # print(f'{"/".join(project_directory.split("/")[:-1])}/icon/{item}.png')
            if os.path.exists(f'{"/".join(project_directory.split("/")[:-1])}/icon/{item}.png'):
                parent.insert("" if directory == project_directory else directory, full_path, item, [],
                              icon=f'icon/{item}.png')
            else:
                parent.insert("" if directory == project_directory else directory, full_path, item, [])
            get_file_tree_data(parent, full_path, project_directory)
        else:
            # print(full_path, item)
            parent.insert("" if directory == project_directory else directory, full_path, item.split(".")[0], [False])


def show_error_popup(error_message):
    log(error_message,"ERROR")
    if error_message.startswith("'Урон"):
        sg.Popup("Брось атаку", location=(200,630), keep_on_top=True,auto_close=True,auto_close_duration=3,no_titlebar=True,background_color="white",text_color="black")
    else:
            sg.Popup("Произошла ошибка", f"Ошибка: {error_message}", title="Ошибка", keep_on_top=True)


# Функция для сохранения данных в JSON файл
def save_values_to_file(values, filename="saved_data.json"):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(values, file, indent=4, ensure_ascii=False)
        # sg.Popup("Данные успешно сохранены!", title="Сохранение")
    except Exception as e:
        sg.Popup("Ошибка при сохранении данных:", f"{e}", title="Ошибка", keep_on_top=True)


# Функция для загрузки данных из JSON файла
def load_values_from_file(filename="saved_data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            values = json.load(file)
        sg.popup_no_buttons("Данные успешно загружены!", auto_close=True, auto_close_duration=1, no_titlebar=True,
                            background_color="#6D6552", location=(650, 250))
        return values
    except FileNotFoundError:
        sg.popup_no_buttons("Файл не найден. Загрузка невозможна.", auto_close=True, auto_close_duration=1,
                            no_titlebar=True, background_color="#6D6552", location=(650, 250))
        return {}
    except Exception as e:
        sg.popup_no_buttons("Ошибка при загрузке данных:", auto_close=True, auto_close_duration=1,
                            no_titlebar=True, background_color="#6D6552", location=(650, 250))
        return {}

def split_dict(input_dict, mode='symbols', limit=50):
    result = []

    if mode == 'symbols':
        current_chunk = {}
        current_length = 0

        for key in input_dict:
            # Учитываем длину ключа + запятую и пробел (кроме первого элемента)
            additional_length = len(key) + (2 if current_chunk else 0)

            if current_length + additional_length > limit:
                result.append(current_chunk)
                current_chunk = {}
                current_length = 0
                additional_length = len(key)  # Для нового чанка не нужно добавлять ", "

            current_chunk[key] = input_dict[key]
            current_length += additional_length

        if current_chunk:
            result.append(current_chunk)

    elif mode == 'count':
        keys = list(input_dict.keys())
        for i in range(0, len(keys), limit):
            chunk_keys = keys[i:i + limit]
            current_chunk = {k: input_dict[k] for k in chunk_keys}
            result.append(current_chunk)

    else:
        raise ValueError("Недопустимый режим. Доступные варианты: 'symbols' или 'count'")

    return result

def multi_string_rectangles(initiative):
    result = []
    max_name_length = max(len(str(key)) for key in initiative.keys())
    total_name_lenght = len("".join([str(key) for key in initiative.keys()]))
    # print(total_name_lenght)
    count_in_row = 160 // max_name_length
    split_result_names = split_dict(initiative, 'count', min(count_in_row, 160))
    start_index = 0
    for rectangles_row in split_result_names:
        result.append(
            create_rectangles(rectangles_row, max_name_length, start_index),
        )
        start_index += len(rectangles_row)
    return [sg.Column(result, key="-RECTANGLES-")]

def create_rectangles(data, max_name_length, start_index=0):
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    # print(data)
    # max_name_length = max(len(str(key)) for key in data.keys())
    return [
        sg.Column([
            # [sg.Push(),sg.Text(index, background_color="green", text_color="black", pad=(1, 0), justification="center",
            #          size=(2, 1),
            #          key=f"rec-{index}-init",border_width=1),sg.Push(),],
            [sg.Push(), sg.Text(key, background_color="green", text_color="black", pad=(1, 0), justification="center",
                                size=(max_name_length, 1),
                                key=f"rec-{start_index + index}-name", border_width=1), sg.Push(), ],
            [sg.Push(),
             sg.Text(str(value), background_color="green", text_color="black", pad=(1, 0), justification="center",
                     size=(2, 1),
                     key=f"rec-{start_index + index}-down", border_width=1), sg.Push(), ]
        ], pad=(1, 0))
        for index, (key, value) in enumerate(sorted_data)
    ]

# keys[i:i + chunk_size] for i in range(0, len(keys), chunk_size)