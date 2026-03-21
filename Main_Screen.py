import ast
import sys
from Witcher_mechanics import *
from Custom_scripts import *
import PySimpleGUI as sg

if getattr(sys, 'frozen', False):
    # Если приложение скомпилировано в .exe
    main_directory = os.path.dirname(sys.executable)
else:
    # Если запускаем как скрипт
    main_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = main_directory + "/enemies_json"
temp_path = "/.temp/temp"
button_size = (14, 1)
button_stat_size = (9, 1)
empty_place = " " * (2 + 1 + button_stat_size[0] + 1) * 2
button_color = [
    ('white', 'blue'), #
    ('white', 'red'), # атакующие
    ('white', 'green'), # защищающие
    ('white', 'purple'), # магические
    ('white', 'orange'), # диологовое
    ('white', 'green')
]


def process_data(input_dict):
    output = {}

    name_keys = [key for key in input_dict if key.startswith("name=")]

    for name_key in name_keys:
        _, number_str = name_key.split("=")
        name = input_dict[name_key]

        suffix = str(int(number_str))
        attributes_dict = {}
        for key in input_dict:
            if key.endswith(suffix) and not key.startswith("name="):
                attribute_key = key[:-len(suffix)]
                attribute_value = input_dict[key]
                attributes_dict[attribute_key] = attribute_value

        output[name] = attributes_dict

    return output


def battle_layout_maker(stats__, added_stats__, skills_, armor_, weapon_, i=0, actor_name='', mining=[""], abilities=[""],
                        weaknes=[""], description=[""], difficult=[""], type_class=""):
    print(actor_name)
    if 'Стрельба из лука' not in skills_:
        skills_['Стрельба из лука'] = 0
    if 'Стрельба из арбалетов' not in skills_:
        skills_['Стрельба из арбалетов'] = 0
    # print(weapon_)
    for key, value in skills_.items():
        skills_[key] = int(value)
    all_skills = {
        "Внимание": 0,
        "Торговля": 0,
        "Дедукция": 0,
        "Образование": 0,
        "Язык: Всеобщий": 0,
        "Язык: Старшая речь": 0,
        "Язык: Краснолюды": 0,
        "Монстрология": 0,
        "Этикет": 0,
        "Ориентирование в городе": 0,
        "Тактика": 0,
        "Передача знаний": 0,
        "Выживание в дикой природе": 0,

        "Борьба": 0,
        "Уклонение/Изворотливость": 0,
        "Ближний бой": 0,
        "Верховая езда": 0,
        "Мореходство": 0,
        "Владение лёгкими клинками": 0,
        "Владение древковым оружием": 0,
        "Владение мечом": 0,

        "Стрельба: Лук": 0,
        "Атлетика": 0,
        "Стрельба: Арбалет": 0,
        "Ловкость рук": 0,
        "Скрытность": 0,

        "Сила": 0,
        "Стойкость": 0,

        "Харизма": 0,
        "Обман": 0,
        "Искусство": 0,
        "Азартные игры": 0,
        "Внешний вид": 0,
        "Понимание людей": 0,
        "Лидерство": 0,
        "Убеждение": 0,
        "Выступление": 0,
        "Соблазнение": 0,

        "Алхимия": 0,
        "Изготовление": 0,
        "Маскировка": 0,
        "Первая помощь": 0,
        "Подделывание": 0,
        "Взлом замков": 0,
        "Знание ловушек": 0,

        "Храбрость": 0,
        "Наведение порчи": 0,
        "Запугивание": 0,
        "Сотворение заклинаний": 0,
        "Сопротивление магии": 0,
        "Сопротивление убеждению": 0,
        "Проведение ритуалов": 0,
    }
    for key, zero in all_skills.items():
        if key not in list(skills_.keys()):
            skills_[key] = zero
    # print(actor_name)
    # for key,value in skills_.items():
    #     if value != 0 and key not in list(all_skills.keys()):
            # print(f"{key} = '{value}'")

    added_stats_ = {"ПЗ": 0,
                    "ВЫН": 0,
                    "БЕГ": 0,
                    "ОТДЫХ": 0,
                    "УСТ": 0,
                    "ЭНЕРГИЯ": 0,
                    "ВЕС": 0, }
    for actor_name, value in added_stats__.items():
        added_stats_[actor_name.upper()] = int(value)
    stats_ = {"ИНТЕЛЛЕКТ": 1,
              "РЕАКЦИЯ": 1,
              "ЛОВКОСТЬ": 1,
              "ТЕЛОСЛОЖЕНИЕ": 1,
              "СКОРОСТЬ": 1,
              "ЭМПАТИЯ": 1,
              "РЕМЕСЛО": 1,
              "ВОЛЯ": 1}
    for key, value in stats__.items():
        # print(name, value)
        stats_[key.upper()] = int(value)
    # print(stats_)
    if len(weapon_) == 2 and type(weapon_) == type(()) and len(str(weapon_)) < 8:
        weapons = [("Что-то", weapon_, "Нет", 0, 1)]
    else:
        weapons = weapon_

    if type(weapons) == type([1]) and len(weapons) == 1:
        weapons = weapons[0]
        weapon_dict = {weapons[0]: (weapons[1], weapons[2], weapons[3], weapons[4])}
    else:
        weapon_dict = {weapon[0]: (weapon[1], weapon[2], weapon[3], weapon[4]) for weapon in weapons}
    l = [list(weapon_dict.values())[0][1:]]
    if type(armor_) in (type(str("")), type(int(0))):
        armor__ = [armor_ for _ in range(6)]
    elif type(armor_) == type([]) and len(armor_) == 1:
        armor__ = [armor_[0] for _ in range(6)]
    else:
        armor__ = armor_
    # for name,value in armor__.items():
    #     armor__[name] = int(value)
    # print(armor__)

    extra_info = {
        "abilities": abilities,
        "weaknes": weaknes,
        "mining": mining,
        "description": description,
    }
    # print(format_text(extra_info[list(extra_info.keys())[0]]))
    return [
        [
            sg.Column([
                [
                    sg.InputText(default_text=actor_name, key=f'name={i}', visible=False, size=(1, 1)),
                    sg.Text("Штраф:"), sg.InputText(default_text="0", key=f'-штраф-{i}', size=(2, 1)),
                    sg.Text("Бонус:"), sg.InputText(
                    default_text="0", key=f'-бонус-{i}', size=(2, 1)),
                    sg.Text(type_class, key=f'type={i}'),
                    sg.Text(", ".join(difficult), key=f'difficult={i}'),
                    # sg.Text(" " * 104),
                    # sg.Text("СВЕТ:"),
                    # sg.Radio("Яркий", "RADIO2", key='light1'),
                    # sg.Radio("Нормальный", "RADIO2", key='light0', default=True),
                    # sg.Radio("Тусклый", "RADIO2", key='light-1'),
                    # sg.Radio("Темнота", "RADIO2", key='light-2'),
                ],
                [
                    sg.InputText(default_text=str(max(0, added_stats_["ПЗ"])), size=(3, 1), key=f'-HP_current-{i}',
                                 enable_events=True), sg.Text("/"),
                    sg.InputText(default_text=str(max(0, added_stats_["ПЗ"])), size=(3, 1), key=f'-HP-{i}'),
                    sg.Button("ПЗ", size=[2, 1], key=f"-HP_restore-{i}"),
                    sg.Text("    "),
                    sg.InputText(default_text=str(max(0, added_stats_["ВЫН"])), size=(3, 1), key=f'-SP-{i}'),
                    sg.Text("/"),
                    sg.InputText(default_text=str(max(0, added_stats_["ВЫН"])), size=(3, 1), key=f'-SP_current-{i}'),
                    sg.Text("ВЫН    "),
                    sg.InputText(default_text=str(max(0, stats_["СКОРОСТЬ"])), size=(3, 1), key=f'-Speed-{i}'),
                    sg.Text("Скорость    "),
                    sg.InputText(default_text=str(max(0, added_stats_["БЕГ"])), size=(3, 1), key=f'-Run_speed-{i}'),
                    sg.Text("Бег    "),
                    sg.InputText(default_text=str(max(0, added_stats_["ОТДЫХ"])), size=(3, 1), key=f'-Rest-{i}'),
                    sg.Text("Отдых    "),
                    sg.InputText(default_text=str(max(0, added_stats_["УСТ"])), size=(3, 1), key=f'-Tired-{i}'),
                    sg.Text("Уст    "),
                    sg.InputText(default_text=str(max(0, added_stats_["ЭНЕРГИЯ"])), size=(3, 1), key=f'-Energy-{i}'),
                    sg.Text("Энергия    "),
                    sg.InputText(default_text=str(stats_.get("УДАЧА", 0)), size=(3, 1), key=f'-Lack-{i}') if stats_.get(
                        "УДАЧА") else sg.Text(""),
                    sg.Text("/") if stats_.get("УДАЧА") else sg.Text(""),
                    sg.InputText(default_text=str(stats_.get("УДАЧА", 0)), size=(3, 1), key=f'-Lack-{i}') if stats_.get(
                        "УДАЧА") else sg.Text(""),
                    sg.Text("Удача    ") if stats_.get("УДАЧА") else sg.Text(""),
                ],
                [
                    sg.InputText(default_text=str(max(0, stats_["ИНТЕЛЛЕКТ"])), key=f"-ИНТЕЛЛЕКТ-{i}", size=(2, 1)),
                    sg.Button("ИНТЕЛЛЕКТ", size=button_stat_size, key=f"b--ИНТЕЛЛЕКТ-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Внимание"])), key=f"-Внимание-{i}", size=(2, 1)),
                    sg.Button("Внимание", size=button_size, key=f"b--Внимание-{i}", button_color=button_color[0]),
                    sg.InputText(default_text=str(max(0, skills_["Торговля"])), key=f"-Торговля-{i}", size=(2, 1)),
                    sg.Button("Торговля", size=button_size, key=f"b--Торговля-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Дедукция"])), key=f"-Дедукция-{i}", size=(2, 1)),
                    sg.Button("Дедукция", size=button_size, key=f"b--Дедукция-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Образование"])), key=f"-Образование-{i}",
                                 size=(2, 1)),
                    sg.Button("Образование", size=button_size, key=f"b--Образование-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Язык: Всеобщий"])), key=f"-Язык: Всеобщий-{i}",
                                 size=(2, 1)),
                    sg.Button("Язык: Всеобщий", size=button_size, key=f"b--Язык: Всеобщий-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Язык: Старшая речь"])),
                                 key=f"-Язык: Старшая речь-{i}",
                                 size=(2, 1)),
                    sg.Button("Язык: Старшая речь", size=button_size, key=f"b--Язык: Старшая речь-{i}"),
                    # sg.InputText(default_text=str(max(0, skills_["Язык: Краснолюды"])), key=f"-Язык: Краснолюды-{i}",
                    #              size=(2, 1)),
                    # sg.Button("Язык: Краснолюды", size=button_size, key=f"b--Язык: Краснолюды-{i}"),
                ],
                [sg.Text(empty_place),
                 sg.InputText(default_text=str(max(0, skills_["Монстрология"])), key=f"-Монстрология-{i}", size=(2, 1)),
                 sg.Button("Монстрология", size=button_size, key=f"b--Монстрология-{i}"),
                 sg.InputText(default_text=str(max(0, skills_["Этикет"])), key=f"-Этикет-{i}", size=(2, 1)),
                 sg.Button("Этикет", size=button_size, key=f"b--Этикет-{i}"),
                 sg.InputText(default_text=str(max(0, skills_["Ориентирование в городе"])),
                              key=f"-Ориентирование в городе-{i}",
                              size=(2, 1)),
                 sg.Button("Ориентирование в городе", size=button_size, key=f"b--Ориентирование в городе-{i}"),
                 sg.InputText(default_text=str(max(0, skills_["Тактика"])), key=f"-Тактика-{i}", size=(2, 1)),
                 sg.Button("Тактика", size=button_size, key=f"b--Тактика-{i}"),
                 sg.InputText(default_text=str(max(0, skills_["Передача знаний"])), key=f"-Передача знаний-{i}",
                              size=(2, 1)),
                 sg.Button("Передача знаний", size=button_size, key=f"b--Передача знаний-{i}"),
                 sg.InputText(default_text=str(max(0, skills_["Выживание в дикой природе"])), key=f"-Выживание-{i}",
                              size=(2, 1)),
                 sg.Button("Выживание", size=button_size, key=f"b--Выживание-{i}"),
                 ],
                [
                    sg.InputText(default_text=str(max(0, stats_["РЕАКЦИЯ"])), key=f"-РЕАКЦИЯ-{i}", size=(2, 1)),
                    sg.Button("РЕАКЦИЯ", size=button_stat_size, key=f"b--РЕАКЦИЯ-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Борьба"])), key=f"-Борьба-{i}", size=(2, 1)),
                    sg.Button("Борьба", size=button_size, key=f"ba-Борьба-{i}", button_color=button_color[1]),
                    sg.InputText(default_text=str(max(0, skills_["Уклонение/Изворотливость"])),
                                 key=f"-Уклонение/Изворотливость-{i}",
                                 size=(2, 1)),
                    sg.Button("Уклонение\nИзворотливость", size=button_size, key=f"b--Уклонение/Изворотливость-{i}",
                              button_color=button_color[2]),
                    sg.InputText(default_text=str(max(0, skills_["Ближний бой"])), key=f"-Ближний бой-{i}",
                                 size=(2, 1)),
                    sg.Button("Ближний бой", size=button_size, key=f"ba-Ближний бой-{i}", button_color=button_color[1]),

                    sg.InputText(default_text=str(max(0, skills_["Владение лёгкими клинками"])),
                                 key=f"-Владение лёгкими клинками-{i}",
                                 size=(2, 1)),
                    sg.Button("Владение лёгкими клинками", size=button_size, key=f"ba-Владение лёгкими клинками-{i}",
                              button_color=button_color[1]),
                    sg.InputText(default_text=str(max(0, skills_["Владение древковым оружием"])),
                                 key=f"-Владение древковым оружием-{i}",
                                 size=(2, 1)),
                    sg.Button("Владение древковым оружием", size=button_size,
                              key=f"ba-Владение древковым оружием-{i}",
                              button_color=button_color[1]),
                    sg.InputText(default_text=str(max(0, skills_["Владение мечом"])), key=f"-Владение мечом-{i}",
                                 size=(2, 1)),
                    sg.Button("Владение мечом", size=button_size, key=f"ba-Владение мечом-{i}",
                              button_color=button_color[1]),

                ],
                [sg.Text(empty_place),
                 sg.InputText(default_text=str(max(0, skills_["Верховая езда"])), key=f"-Верховая езда-{i}",
                              size=(2, 1)),
                 sg.Button("Верховая езда", size=button_size, key=f"b--Верховая езда-{i}"),
                 sg.InputText(default_text=str(max(0, skills_["Мореходство"])), key=f"-Мореходство-{i}",
                              size=(2, 1)),
                 sg.Button("Мореходство", size=button_size, key=f"b--Мореходство-{i}"),

                 ],
                [
                    sg.InputText(default_text=str(max(0, stats_["ЛОВКОСТЬ"])), key=f"-ЛОВКОСТЬ-{i}", size=(2, 1)),
                    sg.Button("ЛОВКОСТЬ", size=button_stat_size, key=f"b--ЛОВКОСТЬ-{i}"),
                    sg.InputText(
                        default_text=str(max(0, max(int(skills_["Стрельба: Лук"]), int(skills_["Стрельба из лука"])))),
                        key=f"-Стрельба: Лук-{i}", size=(2, 1)),
                    sg.Button("Стрельба: Лук", size=button_size, key=f"ba-Стрельба: Лук-{i}",
                              button_color=button_color[1]),
                    sg.InputText(default_text=str(max(0, skills_["Атлетика"])), key=f"-Атлетика-{i}", size=(2, 1)),
                    sg.Button("Атлетика", size=button_size, key=f"b--Атлетика-{i}", button_color=button_color[2]),
                    sg.InputText(
                        default_text=str(
                            max(0, max(int(skills_["Стрельба: Арбалет"]), int(skills_["Стрельба из арбалетов"])))),
                        key=f"-Стрельба: Арбалет-{i}", size=(2, 1)),
                    sg.Button("Стрельба: Арбалет", size=button_size, key=f"ba-Стрельба: Арбалет-{i}",
                              button_color=button_color[1]),
                    sg.InputText(default_text=str(max(0, skills_["Ловкость рук"])), key=f"-Ловкость рук-{i}",
                                 size=(2, 1)),
                    sg.Button("Ловкость рук", size=button_size, key=f"b--Ловкость рук-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Скрытность"])), key=f"-Скрытность-{i}", size=(2, 1)),
                    sg.Button("Скрытность", size=button_size, key=f"b--Скрытность-{i}", button_color=button_color[2]),

                ],
                [
                    sg.InputText(default_text=str(max(0, stats_["ТЕЛОСЛОЖЕНИЕ"])), key=f"-ТЕЛОСЛОЖЕНИЕ-{i}",
                                 size=(2, 1)),
                    sg.Button("ТЕЛО", size=button_stat_size, key=f"b--ТЕЛОСЛОЖЕНИЕ-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Сила"])), key=f"-Сила-{i}", size=(2, 1)),
                    sg.Button("Сила", size=button_size, key=f"b--Сила-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Стойкость"])), key=f"-Стойкость-{i}", size=(2, 1)),
                    sg.Button("Стойкость", size=button_size, key=f"b--Стойкость-{i}",button_color=button_color[2]),

                ],
                [
                    sg.InputText(default_text=str(max(0, stats_["ЭМПАТИЯ"])), key=f"-ЭМПАТИЯ-{i}", size=(2, 1)),
                    sg.Button("ЭМПАТИЯ", size=button_stat_size, key=f"b--ЭМПАТИЯ-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Харизма"])), key=f"-Харизма-{i}", size=(2, 1)),
                    sg.Button("Харизма", size=button_size, key=f"b--Харизма-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Обман"])), key=f"-Обман-{i}", size=(2, 1)),
                    sg.Button("Обман", size=button_size, key=f"b--Обман-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Искусство"])), key=f"-Искусство-{i}", size=(2, 1)),
                    sg.Button("Искусство", size=button_size, key=f"b--Искусство-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Азартные игры"])), key=f"-Азартные игры-{i}",
                                 size=(2, 1)),
                    sg.Button("Азартные игры", size=button_size, key=f"b--Азартные игры-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Внешний вид"])), key=f"-Внешний вид-{i}",
                                 size=(2, 1)),
                    sg.Button("Внешний вид", size=button_size, key=f"b--Внешний вид-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Понимание людей"])), key=f"-Понимание людей-{i}",
                                 size=(2, 1)),
                    sg.Button("Понимание людей", size=button_size, key=f"b--Понимание людей-{i}", button_color=button_color[0]),

                ],
                [sg.Text(empty_place),
                 sg.InputText(default_text=str(max(0, skills_["Лидерство"])), key=f"-Лидерство-{i}", size=(2, 1)),
                 sg.Button("Лидерство", size=button_size, key=f"b--Лидерство-{i}"),
                 sg.InputText(default_text=str(max(0, skills_["Убеждение"])), key=f"-Убеждение-{i}", size=(2, 1)),
                 sg.Button("Убеждение", size=button_size, key=f"b--Убеждение-{i}"),
                 sg.InputText(default_text=str(max(0, skills_["Выступление"])), key=f"-Выступление-{i}", size=(2, 1)),
                 sg.Button("Выступление", size=button_size, key=f"b--Выступление-{i}"),
                 sg.InputText(default_text=str(max(0, skills_["Соблазнение"])), key=f"-Соблазнение-{i}", size=(2, 1)),
                 sg.Button("Соблазнение", size=button_size, key=f"b--Соблазнение-{i}"),

                 ],
                [
                    sg.InputText(default_text=str(max(0, stats_["РЕМЕСЛО"])), key=f"-РЕМЕСЛО-{i}", size=(2, 1)),
                    sg.Button("РЕМЕСЛО", size=button_stat_size, key=f"b--РЕМЕСЛО-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Алхимия"])), key=f"-Алхимия-{i}", size=(2, 1)),
                    sg.Button("Алхимия", size=button_size, key=f"b--Алхимия-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Изготовление"])), key=f"-Изготовление-{i}",
                                 size=(2, 1)),
                    sg.Button("Изготовление", size=button_size, key=f"b--Изготовление-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Маскировка"])), key=f"-Маскировка-{i}", size=(2, 1)),
                    sg.Button("Маскировка", size=button_size, key=f"b--Маскировка-{i}", button_color=button_color[2]),
                    sg.InputText(default_text=str(max(0, skills_["Первая помощь"])), key=f"-Первая помощь-{i}",
                                 size=(2, 1)),
                    sg.Button("Первая помощь", size=button_size, key=f"b--Первая помощь-{i}"),
                    # sg.InputText(default_text=str(max(0, skills_["Подделывание"])), key=f"-Подделывание-{i}", # todo
                    #              size=(2, 1)),
                    # sg.Button("Подделывание", size=button_size, key=f"b--Подделывание-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Взлом замков"])), key=f"-Взлом замков-{i}",
                                 size=(2, 1)),
                    sg.Button("Взлом замков", size=button_size, key=f"b--Взлом замков-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Знание ловушек"])), key=f"-Знание ловушек-{i}",
                                 size=(2, 1)),
                    sg.Button("Знание ловушек", size=button_size, key=f"b--Знание ловушек-{i}"),

                ],
                [
                    sg.InputText(default_text=str(max(0, stats_["ВОЛЯ"])), key=f"-ВОЛЯ-{i}", size=(2, 1)),
                    sg.Button("ВОЛЯ", size=button_stat_size, key=f"b--ВОЛЯ-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Храбрость"])), key=f"-Храбрость-{i}", size=(2, 1)),
                    sg.Button("Храбрость", size=button_size, key=f"b--Храбрость-{i}"),
                    # sg.InputText(default_text=str(max(0, skills_["Наведение порчи"])), key=f"-Наведение порчи-{i}", # todo
                    #              size=(2, 1)),
                    # sg.Button("Наведение порчи", size=button_size, key=f"b--Наведение порчи-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Запугивание"])), key=f"-Запугивание-{i}",
                                 size=(2, 1)),
                    sg.Button("Запугивание", size=button_size, key=f"b--Запугивание-{i}"),
                    sg.InputText(default_text=str(max(0, skills_["Сотворение заклинаний"])),
                                 key=f"-Сотворение заклинаний-{i}",
                                 size=(2, 1)),
                    sg.Button("Сотворение заклинаний", size=button_size, key=f"b--Сотворение заклинаний-{i}",
                              button_color=button_color[1]),
                    sg.InputText(default_text=str(max(0, skills_["Сопротивление магии"])),
                                 key=f"-Сопротивление магии-{i}",
                                 size=(2, 1)),
                    sg.Button("Сопротивление магии", size=button_size, key=f"b--Сопротивление магии-{i}",button_color=button_color[2]),
                    sg.InputText(default_text=str(max(0, skills_["Сопротивление убеждению"])),
                                 key=f"-Сопротивление убеждению-{i}",
                                 size=(2, 1)),
                    sg.Button("Сопротивление убеждению", size=button_size, key=f"b--Сопротивление убеждению-{i}", button_color=button_color[2]),
                    sg.InputText(default_text=str(max(0, skills_["Проведение ритуалов"])),
                                 key=f"-Проведение ритуалов-{i}",
                                 size=(2, 1)),
                    sg.Button("Проведение ритуалов", size=button_size, key=f"b--Проведение ритуалов-{i}"),
                ],

                [
                    sg.Multiline(size=(20, 5), key=f'-OUTPUT-{i}', disabled=True),
                    sg.Column([
                        [
                            sg.Text("Защита:", background_color=button_color[2][1], text_color=button_color[1][0]),
                            sg.InputText(size=(3, 1), key=f"-defense-{i}", background_color=button_color[2][1],
                                         text_color=button_color[1][0]),
                            sg.Text("Броня:", background_color=button_color[2][1], text_color=button_color[1][0]),
                            sg.InputText(0, size=(3, 1), key=f"-armor-{i}", background_color=button_color[2][1],
                                         text_color=button_color[1][0])
                        ],
                        [
                            sg.Button('Урон', button_color=button_color[1], key=f"b-Урон-{i}"),
                            sg.InputText(list(weapon_dict.values())[0][0][0], size=(2, 1), key=f"-damage_roll-{i}"),
                            sg.Text("d6+"),
                            sg.InputText(list(weapon_dict.values())[0][0][1], size=(2, 1), key=f"-add_damage-{i}"),
                            sg.Text(f"{"+"+str(((max(0, stats_["ТЕЛОСЛОЖЕНИЕ"]) - 5) // 2) * 2) if ((max(0, stats_["ТЕЛОСЛОЖЕНИЕ"]) - 5) // 2) * 2 >=0 else ((max(0, stats_["ТЕЛОСЛОЖЕНИЕ"]) - 5) // 2) * 2}",
                                    key=f"b-add_damage_physique-{i}"),
                            sg.Checkbox("ББ", default=True, key=f"c-add_damage_physique_flag-{i}")
                        ],
                        [
                            sg.Combo(list(weapon_dict.keys()), default_value=list(weapon_dict.keys())[0], size=(23, 1),
                                     key=f"-COMBO-{i}", enable_events=True)
                        ]
                    ]),
                    sg.Table(values=l, headings=["Эффект", "Точно", "СА"], key=f"-TABLE-{i}", auto_size_columns=False,
                             col_widths=[20, 5, 3],
                             hide_vertical_scroll=True, num_rows=4, justification="center", metadata=weapon_dict),
                    sg.Column([
                        [
                            sg.InputText(default_text=armor__[0], key=f'-armor_head-{i}', size=(2, 1)),
                            sg.Text("Голова"),
                            sg.InputText(default_text=armor__[1], key=f'-armor_body-{i}', size=(2, 1)),
                            sg.Text("Тело"),
                            sg.InputText(default_text=armor__[2], key=f'-armor_r_h-{i}', size=(2, 1)),
                            sg.Text("П.Р."),
                            sg.InputText(default_text=armor__[3], key=f'-armor_l_h-{i}', size=(2, 1)),
                            sg.Text("Л.Р."),
                            sg.InputText(default_text=armor__[4], key=f'-armor_r_l-{i}', size=(2, 1)),
                            sg.Text("П.Н."),
                            sg.InputText(default_text=armor__[5], key=f'-armor_l_l-{i}', size=(2, 1)),
                            sg.Text("Л.Н."),
                            # sg.Text("<--- Броня")
                        ],
                        [
                            sg.Radio(" Голова", f"RADIO1{i}", key=f'Голова-{i}'),
                            sg.Radio(" Тело", f"RADIO1{i}", key=f'Тело-{i}'),
                            sg.Radio(" П.Р.", f"RADIO1{i}", key=f'П.Р.-{i}'),
                            sg.Radio(" Л.Р.", f"RADIO1{i}", key=f'Л.Р.-{i}'),
                            sg.Radio(" П.Н.", f"RADIO1{i}", key=f'П.Н.-{i}'),
                            sg.Radio(" Л.Н.", f"RADIO1{i}", key=f'Л.Н.-{i}'),
                        ],
                        [
                            sg.Radio("Random", f"RADIO1{i}", key=f'random-{i}', default=True)
                        ],
                    ])
                ]

            ]),
            sg.Column(
                [
                    [sg.Combo(list(extra_info.keys()), default_value=list(extra_info.keys())[0],
                              key=f"-EXTRA_INFO_COMBO-{i}", enable_events=True, size=(40, 1), metadata=extra_info)],
                    [sg.Multiline(format_text(extra_info[list(extra_info.keys())[0]], max_length=40), size=(40, 28),
                                  key=f"-EXTRA_INFO-{i}",
                                  background_color="lightgray",
                                  autoscroll=True, enable_events=False)]
                ]
                , vertical_alignment='top')]
    ]


def main():
    skills_to_attributes = {
        "Внимание": "ИНТЕЛЛЕКТ",
        "Выживание в дикой природе": "ИНТЕЛЛЕКТ",
        "Дедукция": "ИНТЕЛЛЕКТ",
        "Монстрология": "ИНТЕЛЛЕКТ",
        "Образование": "ИНТЕЛЛЕКТ",
        "Ориентирование в городе": "ИНТЕЛЛЕКТ",
        "Передача знаний": "ИНТЕЛЛЕКТ",
        "Тактика": "ИНТЕЛЛЕКТ",
        "Торговля": "ИНТЕЛЛЕКТ",
        "Этикет": "ИНТЕЛЛЕКТ",
        "Язык": "ИНТЕЛЛЕКТ",

        "Ближний бой": "РЕАКЦИЯ",
        "Борьба": "РЕАКЦИЯ",
        "Верховая езда": "РЕАКЦИЯ",
        "Владение древковым оружием": "РЕАКЦИЯ",
        "Владение лёгкими клинками": "РЕАКЦИЯ",
        "Владение мечом": "РЕАКЦИЯ",
        "Мореходство": "РЕАКЦИЯ",
        "Уклонение/Изворотливость": "РЕАКЦИЯ",

        "Атлетика": "ЛОВКОСТЬ",
        "Ловкость рук": "ЛОВКОСТЬ",
        "Скрытность": "ЛОВКОСТЬ",
        "Стрельба: Арбалет": "ЛОВКОСТЬ",
        "Стрельба: Лук": "ЛОВКОСТЬ",

        "Сила": "ТЕЛОСЛОЖЕНИЕ",
        "Стойкость": "ТЕЛОСЛОЖЕНИЕ",

        "Азартные игры": "ЭМПАТИЯ",
        "Внешний вид": "ЭМПАТИЯ",
        "Выступление": "ЭМПАТИЯ",
        "Искусство": "ЭМПАТИЯ",
        "Лидерство": "ЭМПАТИЯ",
        "Обман": "ЭМПАТИЯ",
        "Понимание людей": "ЭМПАТИЯ",
        "Соблазнение": "ЭМПАТИЯ",
        "Убеждение": "ЭМПАТИЯ",
        "Харизма": "ЭМПАТИЯ",

        "Алхимия": "РЕМЕСЛО",
        "Взлом замков": "РЕМЕСЛО",
        "Знание ловушек": "РЕМЕСЛО",
        "Изготовление": "РЕМЕСЛО",
        "Маскировка": "РЕМЕСЛО",
        "Первая помощь": "РЕМЕСЛО",
        "Подделывание": "РЕМЕСЛО",

        "Храбрость": "ВОЛЯ",
        "Наведение порчи": "ВОЛЯ",
        "Запугивание": "ВОЛЯ",
        "Проведение ритуалов": "ВОЛЯ",
        "Сопротивление магии": "ВОЛЯ",
        "Сопротивление убеждению": "ВОЛЯ",
        "Сотворение заклинаний": "ВОЛЯ"

    }
    # Кастомная тема
    # Создаем новую тему
    # sg.theme_add_new('Parchment', {
    #     'BACKGROUND': '#deb975',  # Цвет фона, напоминающий пергамент (wheat)
    #     'TEXT': '#000000',  # Темно-коричневый цвет текста
    #     'INPUT': '#deb975',  # Цвет полей ввода, совпадает с фоном для стилизации под "скрытое поле"
    #     'TEXT_INPUT': '#000000',  # Темно-коричневый цвет текста в полях ввода
    #     'SCROLL': '#5b3a29',  # Цвет скроллбаров
    #     'BUTTON': ('#deb975', '#5b3a29'),  # Пергаментный фон с темным текстом на кнопках
    #     'PROGRESS': ('#deb975', '#5b3a29'),  # Прогресс бар
    #     'BORDER': 1,
    #     'SLIDER_DEPTH': 0,
    #     'PROGRESS_DEPTH': 0,
    # })

    # Установка новой темы
    sg.theme('DarkGrey2')
    # Применяем свою тему
    # sg.theme('GrayGrayGray')
    # sg.theme('Default1')
    target_list = {'Голова': -6, 'Тело': -1, 'П.Р.': -3, 'Л.Р.': -3, 'П.Н.': -2, 'Л.Н.': -2, 'random': 0}
    l = ['Голова', 'Тело', 'Тело', 'Тело', 'П.Р.', 'Л.Р.', 'П.Н.', 'П.Н.', 'Л.Н.', 'Л.Н.']
    file_tree = sg.TreeData()
    file_tree.select_mode = sg.SELECT_MODE_MULTIPLE
    # Задайте начальную директорию для вашего проекта

    project_directory = main_directory + "/Enemies_json"

    # Заполнение дерева файловой системой
    get_file_tree_data(file_tree, project_directory, project_directory)
    layout = [
        [sg.Tree(data=file_tree, headings=[], auto_size_columns=True, num_rows=20, col0_width=40,
                 select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                 key='-TREE-', show_expanded=False, enable_events=True)],
        [sg.Text(text="", key='-selected-')],
        [sg.Button("Бой"),
         sg.Button("Добавить/Убрать"),
         sg.Button("Выход")]
    ]

    menu_window = sg.Window("Выбор актёров", layout, finalize=True, icon='icon/icon.ico')
    selected_full = list(load_values_from_file("selected.json"))
    # print(selected_full)
    # selected_full = []
    selected = []
    for selected_item in selected_full:
        selected.append(selected_item.split("/")[-1].split(".")[0])
    menu_window.Element('-selected-').update(format_text(', '.join((selected)) + ".", 50))
    log("Battle start","MENU")
    values = None
    while True:
        # try:
        menu_event, menu_values = menu_window.read()
        log(menu_event,"MENU")
        if menu_event == sg.WIN_CLOSED or menu_event == "Выход":
            break
        if menu_event == "Добавить/Убрать" and menu_values['-TREE-'] != []:
            actor_path = menu_values['-TREE-'][0]
            actor_name = actor_path.split("/")[-1].split(".")[0]
            # print(actor_path)

            if actor_name in ", ".join(selected):
                for i in range(len(selected) - 1, -1, -1):
                    if actor_name in selected[i]:
                        selected.remove(selected[i])
                        selected_full.remove(selected_full[i])
            else:
                num_copies = ""
                while not num_copies.isdigit():
                    num_copies = sg.popup_get_text(f"Сколько копий для {actor_name}?", "Копии актёра", default_text="1",
                                                   size=(2, 3))
                    if num_copies and num_copies.isdigit():
                        if int(num_copies) == 1:
                            selected.append(actor_name)
                            selected_full.append(actor_path)
                        else:
                            for i in range(int(num_copies)):
                                selected.append("№" + str(i + 1) + " " + actor_name)
                                selected_full.append(str(actor_path)[:-(3 + len(actor_name))] + "№" + str(
                                    i + 1) + " " + actor_name + ".py")
                    if num_copies is None:
                        break

            menu_window.Element('-selected-').update(format_text(', '.join((selected)) + ".", 50))
        if menu_event == "Бой" and len(selected) != 0:
            tabs_names = list(enumerate(selected,1))
            log(f"Порядок: {tabs_names}")
            save_values_to_file(selected_full, "selected.json")
            initiative = {}
            with open(main_directory + temp_path, "w", encoding="utf-8") as f:  # очистка файла todo: точно надо? НАДО!
                f.write("")

            for select in selected_full:
                # Заменяем .py на .json
                json_file_path = select.replace('.py', '.json')

                try:
                    # Используем новую функцию загрузки из Custom_scripts
                    enemy_tuple = load_enemy_from_json(json_file_path)

                    # Записываем в temp файл
                    with open(main_directory + temp_path, "a", encoding="utf-8") as f:
                        f.write(str(enemy_tuple) + "\n")

                    # Добавляем в инициативу
                    enemy_name = os.path.basename(json_file_path).replace('.json', '')
                    initiative[enemy_name] = 0

                    log(f"Загружен враг: {enemy_name}", "INFO")

                except FileNotFoundError as e:
                    log(f"Ошибка загрузки: {e}", "ERROR")
                    sg.Popup(f"Ошибка загрузки врага:\n{e}\n\nФайл будет пропущен.",
                             title="Ошибка", keep_on_top=True)
                    continue
                except Exception as e:
                    log(f"Неизвестная ошибка при загрузке {select}: {e}", "ERROR")
                    sg.Popup(f"Ошибка при загрузке врага:\n{e}\n\nФайл будет пропущен.",
                             title="Ошибка", keep_on_top=True)
                    continue
            #
            # for select in selected_full:
            #     print(select)
            #     if "№" in select:
            #         #                     # print(1, select.split(" №")[0] + ".py")
            #         #                     with open(select.split(" №")[0] + ".py", "r",
            #         #                               encoding="utf-8") as f:  # если в select есть № то мы дую
            #         #                         save_exec(f.read())
            #         # print(1, select.split("№")[1][1:] + ".py")
            #         with open(select.split("№")[0] + "/" + select.split("№")[1][2:], "r",
            #                   encoding="utf-8") as f:  # если в select есть № то мы дую
            #             save_exec(f.read())
            #
            #     else:
            #         # print(2, select)
            #         with open(select, "r", encoding="utf-8") as f:
            #             save_exec(f.read())
            #             # print(f.read().splitlines()[-1])
                initiative[select.split("/")[-1].split(".")[0]] = 0
            # print(initiative)
            current_in_initiative = (selected_full[0].split("/")[-1].split(".")[0], 0)
            with open(main_directory + temp_path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
            print(lines)
            # print(split_result)
            for index, line in enumerate(lines):
                real_line = ast.literal_eval(line)
                if lines.count(real_line[-2]) > 1:
                    real_line[-2] = real_line[-2] + "№" + lines.count(real_line[-2])
                    lines[index] = str(real_line)
            layout_2 = [
                [sg.Button('Инициатива'),
                 sg.Text(f"Ход: {current_in_initiative[0].replace("_", "")} = {current_in_initiative[1]}",
                         key="-current_in_initiative-"),
                 sg.Button('Следующий ход'),
                 sg.Combo(["Муж", "Жен", "Люб"], default_value="Люб", key='-SEX-COMBO-'),
                 sg.Combo(["Север", "Туссент", "Aen Seidhe", "Краснолюд", "Люб"], default_value="Люб",
                          key='-RACE-COMBO-'),
                 sg.Button('Случайное имя', key="-random_name_button-"),
                 sg.Text(' ' * 22, key="-random_name-"),
                 sg.Combo(loaded_data["personal_items_types"], default_value="Обычные", key='-RARITY-COMBO-'),
                 sg.Button('Случайная вещь', key="-random_item_button-"),
                 sg.Text('               ', key="-random_item-")],
                # sg.InputText("Не забывай просить бросать кубы",size=(20, 1), key=f'--'),
                # [sg.Text(', '.join(f"{key}: {value}" for key, value in initiative.items()),
                #          key="-initiative-")],
                multi_string_rectangles(initiative),
                [sg.TabGroup([
                    [  # Нужно убрать этот лишний список
                        sg.Tab(
                            'Мастерская Вкладка', [
                                # [sg.Text('Генератор NPC для ведущего', font=('Arial', 16, 'bold'))],
                                [sg.Text('Нажмите кнопку для генерации случайного персонажа:'),
                                 sg.Button('Сгенерировать персонажа', key='-generate_char-'),
                                 sg.Button('Сгенерировать Скоятаэля', key='-generate_char_scoiatael-')],
                                [
                                    sg.Multiline(size=(154, 13), key='-CHAR_OUTPUT-',
                                                 autoscroll=False, enable_events=False),
                                    sg.Column([
                                        [sg.Table(
                                            values=[
                                                ["<0", "35%", "120%"],
                                                ["1-3", "50%", "100%"],
                                                ["4-5", "65%", "85%"],
                                                ["6-7", "75%", "75%"],
                                                ["8-9", "85%", "65%"],
                                                ["10+", "100%", "50%"]
                                            ],
                                            headings=['>СЛ', 'Цена продажи', 'Цена покупки'],
                                            max_col_width=30,
                                            auto_size_columns=False,
                                            col_widths=[5, 10, 10],
                                            hide_vertical_scroll=True,
                                            justification='center',
                                            key='-TRADING_TABLE-',
                                            row_height=15,
                                            num_rows=5,
                                        )],
                                        [sg.Text("Основа"), sg.InputText(default_text=5, key=f"-FREE_ROLL_BASE-",
                                                                         size=(2, 1)),
                                         sg.Button("Бросок", size=button_stat_size, key=f"--FREE_ROLL-", ),
                                         sg.InputText(size=(2, 1), key="-FREE_ROLL_OUTPUT-")],
                                    ])
                                ],
                                [sg.Table(
                                    values=race_features_data,
                                    headings=race_features_headings,
                                    max_col_width=50,
                                    auto_size_columns=False,
                                    col_widths=[10, 10, 20, 12, 12, 10, 12, 15, 50],
                                    row_height=40,
                                    hide_vertical_scroll=True,
                                    # display_row_numbers=True,
                                    justification='left',
                                    num_rows=min(10, len(race_features_data)),
                                    # vertical_scroll_only=False,
                                    # enable_events=True,
                                    key='-RACE_TABLE-',
                                    # expand_x=True,
                                    # expand_y=True,

                                )],
                                # [sg.Button('Очистить', key='-CLEAR_CHAR-'), sg.Button('Копировать', key='-COPY_CHAR-')]
                            ]
                        )
                        ,
                        # sg.Tab('Особенности рас', [
                        #     [sg.Table(
                        #     values=race_features_data,
                        #     headings=race_features_headings,
                        #     max_col_width=50,
                        #     auto_size_columns=False,
                        #     col_widths=[12, 12, 15, 15, 20, 12, 12, 10, 10, 10, 20],
                        #     display_row_numbers=True,
                        #     justification='left',
                        #     num_rows=min(10, len(race_features_data)),
                        #     vertical_scroll_only=False,
                        #     enable_events=True,
                        #     key='-RACE_TABLE-',
                        #     row_height=30,
                        #     expand_x=True,
                        #     expand_y=True
                        # )]],)
                    ] + [  # Объединяем с другими вкладками
                        sg.Tab(
                            selected[i],
                            battle_layout_maker(ast.literal_eval(lines[i])[0], ast.literal_eval(lines[i])[1],
                                                ast.literal_eval(lines[i])[2], ast.literal_eval(lines[i])[3],
                                                ast.literal_eval(lines[i])[5], i, selected[i])
                        ) if len(ast.literal_eval(lines[i])) == 6 else
                        sg.Tab(
                            selected[i],
                            battle_layout_maker(ast.literal_eval(lines[i])[0], ast.literal_eval(lines[i])[1],
                                                ast.literal_eval(lines[i])[2], ast.literal_eval(lines[i])[3],
                                                ast.literal_eval(lines[i])[5], i, selected[i],
                                                ast.literal_eval(lines[i])[6], ast.literal_eval(lines[i])[7],
                                                ast.literal_eval(lines[i])[8], ast.literal_eval(lines[i])[9],
                                                ast.literal_eval(lines[i])[10], ast.literal_eval(lines[i])[11])
                        )
                        for i in range(len(lines))
                    ]
                ]),
                    # sg.Output(size=(2, 30), )  # TODO
                ],
                [sg.Button('Назад'),
                 sg.Multiline(size=(188, 3), key=f'-NOTES-', autoscroll=True, enable_events=False),
                 ]
            ]
            menu_window.hide()
            print()
            window = sg.Window(f'Бой', layout_2, finalize=True, icon='icon/icon.ico')
            roll = None
            # Создание директории для временных файлов
            temp_dir = ".temp"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            saved_data = load_values_from_file(".temp/saved_data.json")
            if saved_data is not None:
                saved_data.pop("0", None)
                saved_data = process_data(saved_data)
                all_keys = window.AllKeysDict.keys()
                for name, features in saved_data.items():
                    if name in selected:
                        i_new = str(selected.index(name))
                        for key, value in features.items():
                            if key not in ["-TABLE-"]:
                                if f'{key}{i_new}' in all_keys:
                                    window[f'{key}{i_new}'].update(value)
                            else:
                                weapon_dict = window.Element(f"-TABLE-{i_new}").metadata
                                weapon_index = list(weapon_dict.keys()).index(features[f"-COMBO-"])
                                window[f"-TABLE-{i_new}"].update([list(weapon_dict.values())[weapon_index][1:]])
            for i in range(len(selected)):
                initial_values = {
                    f'-HP_current-{i}': window[f'-HP_current-{i}'].get(),
                    f'-HP-{i}': window[f'-HP-{i}'].get(),
                }
                if float(initial_values[f'-HP_current-{i}']) < float(initial_values[f'-HP-{i}']) // 5 or float(
                        initial_values[f'-HP_current-{i}']) == 0:
                    window[f"rec-{i}-name"].update(background_color="red")
                    window[f"rec-{i}-down"].update(background_color="red")
                elif float(initial_values[f'-HP_current-{i}']) < float(initial_values[f'-HP-{i}']) // 2:
                    window[f"rec-{i}-name"].update(background_color="yellow")
                    window[f"rec-{i}-down"].update(background_color="yellow")
                elif float(initial_values[f'-HP_current-{i}']) < float(initial_values[f'-HP-{i}']):
                    window[f"rec-{i}-name"].update(background_color="palegreen")
                    window[f"rec-{i}-down"].update(background_color="palegreen")
                else:
                    window[f"rec-{i}-name"].update(background_color="green")
                    window[f"rec-{i}-down"].update(background_color="green")

            while True:
                try:
                    if not window.was_closed():
                        event, values = window.read()
                    else:
                        # Window is closed, break out of the loop
                        break
                    log(f"{values[event[2:]] if event[2:] in dict(values).keys() else ""}{values[event[1:]] if event[1:] in dict(values).keys() else ""} ({event})")
                    # print(event, values)
                    if event in (sg.WIN_CLOSED, 'Назад'):
                        if values:
                            save_values_to_file(values)
                        break

                    tab_event = event.split("-")[-1]
                    event_value = ""
                    if event[0] == "b":
                        event_value = event[2:].replace(tab_event, '')[:-1]
                        stats_value = int(values["-" + str(
                            skills_to_attributes[
                                event_value.replace("-", "")]) + "-" + tab_event] if event_value.replace(
                            "-", "") in skills_to_attributes.keys() else 0)
                    if event[1] == "a":
                        # if any(values[f"{radio_key}-{tab_event}"] for radio_key in target_list.keys()):
                        accuracy = window.Element(f"-TABLE-{tab_event}").Values
                        selected_radio = next(
                            (radio_key for radio_key in target_list.keys() if values[f"{radio_key}-{tab_event}"]),
                            "random"  # Возвращается, если ничего не найдено
                        )
                        roll = special_d10_roll() + target_list[selected_radio] + accuracy[0][1]
                        if selected_radio == "random":
                            target = \
                                ['Голова', 'Тело', 'Тело', 'Тело', 'П.Р.', 'Л.Р.', 'П.Н.', 'П.Н.', 'Л.Н.', 'Л.Н.'][
                                    roll_d10(False) - 1]
                        else:
                            target = selected_radio
                        roll = roll + int(values[event[2:]]) + stats_value - int(
                            values[f'-штраф-{tab_event}']) + int(
                            values[f'-бонус-{tab_event}'])
                        damage_mod = ['x3', 'x1', 'x1', 'x1', 'x1/2', 'x1/2', 'x1/2', 'x1/2', 'x1/2', 'x1/2'][
                            l.index(target)]
                        window[f'-OUTPUT-{tab_event}'].update(
                            f"Попадание: {roll}\nЦель: {target}\nУрон: {damage_mod}\n", append=True)
                        window[f'-OUTPUT-{tab_event}'].Widget.yview_moveto(1.0)
                    elif event == f"--FREE_ROLL-":
                        window[f'-FREE_ROLL_OUTPUT-'].update(int(values['-FREE_ROLL_BASE-']) + special_d10_roll())
                    elif event_value == 'Урон' and roll is not None and roll < int(values[f"-defense-{tab_event}"]):
                        if roll < int(values[f"-defense-{tab_event}"]):
                            window[f'-OUTPUT-{tab_event}'].update("Мимо\n", append=True)
                            window[f'-OUTPUT-{tab_event}'].Widget.yview_moveto(1.0)
                    elif event_value == 'Урон' and roll is not None:
                        damage = int(values[f"-add_damage-{tab_event}"])
                        if values[f"c-add_damage_physique_flag-{tab_event}"]:
                            damage += ((max(0, int(values[f"-ТЕЛОСЛОЖЕНИЕ-{tab_event}"])) - 5) // 2) * 2
                        for i in range(int(values[f"-damage_roll-{tab_event}"])):
                            damage += roll_d6()
                        print("--")
                        flag = True
                        if values[f"-defense-{tab_event}"] is not None and values[f"-defense-{tab_event}"] != '':
                            # if roll == int(values[f"-defense-{tab_event}"]):
                            #     window[f'-OUTPUT-{tab_event}'].update("Вскользь\n", append=True)
                            #     window[f'-OUTPUT-{tab_event}'].Widget.yview_moveto(1.0)
                            #     damage = round(damage / 2)
                            # if damage - int(values[f"-armor-{tab_event}"]) <= 0 and flag:
                            #     window[f'-OUTPUT-{tab_event}'].update(f"Нет пробития\n", append=True)
                            #     window[f'-OUTPUT-{tab_event}'].Widget.yview_moveto(1.0)
                            # else:
                            if flag:
                                    window[f'-OUTPUT-{tab_event}'].update(f"Пробитие брони.\n", append=True)
                                    damage += crit_damage(roll, int(values[f"-defense-{tab_event}"]), target, window,
                                                          tab_event)
                                    damage = {'x3': damage * 3, 'x1': damage, 'x1/2': damage / 2}[damage_mod]
                                    damage -= int(values[f"-armor-{tab_event}"])
                                    window[f'-OUTPUT-{tab_event}'].update(f"Урон: {round(max(damage, 0))}\n",
                                                                          append=True)
                                    window[f'-OUTPUT-{tab_event}'].Widget.yview_moveto(1.0)
                    elif event == f"-COMBO-{tab_event}":
                        weapon_dict = window.Element(f"-TABLE-{tab_event}").metadata
                        # selected_weapon = weapon_dict[values[f"-COMBO-{tab_event}"]]
                        weapon_index = list(weapon_dict.keys()).index(values[f"-COMBO-{tab_event}"])
                        # print(list(weapon_dict.keys()), values[f"-COMBO-{tab_event}"], selected_weapon, )
                        window[f"-TABLE-{tab_event}"].update([list(weapon_dict.values())[weapon_index][1:]])
                        window[f"-damage_roll-{tab_event}"].update(
                            int(list(weapon_dict.values())[weapon_index][0][0]))
                        window[f"-add_damage-{tab_event}"].update(
                            int(list(weapon_dict.values())[weapon_index][0][1]))
                    elif event[0] == "b":
                        window[f'-OUTPUT-{tab_event}'].update(
                            f"Бросок {event_value.replace("-","")}: {special_d10_roll() + int(values[event[2:]]) + stats_value - int(values[f'-штраф-{tab_event}']) + int(values[f'-бонус-{tab_event}'])}\n",
                            append=True)
                        window[f'-OUTPUT-{tab_event}'].Widget.yview_moveto(1.0)
                    elif event == "Инициатива":
                        for i, (k, v) in enumerate(initiative.items()):
                            initiative[k] = special_d10_roll() + int(values[f"-РЕАКЦИЯ-{i}"])
                        initiative = dict(sorted(initiative.items(), key=lambda item: item[1], reverse=True))
                        # print(initiative)
                        current_in_initiative = (list(initiative.keys())[0], initiative[list(initiative.keys())[0]])
                        # window.Element('-initiative-').update(str(initiative))
                        window.Element('-current_in_initiative-').update(
                            f"Ход: {current_in_initiative[0].replace("_", "")} = {current_in_initiative[1]}")
                        items = list(initiative.items())
                        window[current_in_initiative[0]].select()
                        update_rectangles(window, initiative, selected, values)
                        # print(items)
                        log(f"Инициатива: {list(map(lambda x: (x[1], x[0]), items))}")
                    elif event == "Следующий ход":
                        current_index = items.index(current_in_initiative)
                        if current_index + 1 < len(items):
                            current_in_initiative = (items[current_index + 1])
                        else:
                            current_in_initiative = (items[0])
                        window.Element('-current_in_initiative-').update(
                            f"Ход: {current_in_initiative[0].replace("_", "")} = {current_in_initiative[1]}")
                        window[current_in_initiative[0]].select()
                    elif event == f"-HP_restore-{tab_event}":
                        window[f'-HP_current-{tab_event}'].update(values[f'-HP-{tab_event}'])
                        changed_element = list(initiative.keys()).index(selected[int(tab_event)])
                        window[f"rec-{changed_element}-name"].update(background_color="green")
                        window[f"rec-{changed_element}-down"].update(background_color="green")
                    elif event == f"-generate_char-":
                        character_description = generate_character_description()
                        current_text = window['-CHAR_OUTPUT-'].get()
                        if current_text:
                            new_text = f"{character_description}\n\n{'-' * 50}\n\n{current_text}"
                        else:
                            new_text = character_description
                        log(character_description.replace("\n"," # "))
                        window['-CHAR_OUTPUT-'].update(new_text)
                    elif event == f"-generate_char_scoiatael-":
                        character_description = generate_scoiatael()
                        current_text = window['-CHAR_OUTPUT-'].get()
                        if current_text:
                            new_text = f"{character_description}\n\n{'-' * 50}\n\n{current_text}"
                        else:
                            new_text = character_description
                        log(character_description.replace("\n", " # "))
                        window['-CHAR_OUTPUT-'].update(new_text)
                    elif event == f"-random_name_button-":
                        window[f'-random_name-'].update(
                            random_name(values['-SEX-COMBO-'], values['-RACE-COMBO-']).ljust(22))
                    elif event == f"-random_item_button-":
                        window[f'-random_item-'].update(random_things(values['-RARITY-COMBO-']))
                    elif event == f"-EXTRA_INFO_COMBO-{tab_event}":  # Обработка выбора в выпадающем списке
                        selected_option = values[f"-EXTRA_INFO_COMBO-{tab_event}"]
                        if selected_option:
                            window[f"-EXTRA_INFO-{tab_event}"].update(
                                format_text(window[event].metadata[selected_option]))
                    # print(event)
                    if event.startswith("-HP_current-"):
                        hp_sp_total = []
                        for i_tab,name_tab in tabs_names:
                            hp_sp_total.append(f"ХП {name_tab} = {values[f'-HP_current-{i_tab-1}']}/{values[f'-HP-{i_tab-1}']}")
                            hp_sp_total.append(f"ПЗ {name_tab} = {values[f'-SP_current-{i_tab-1}']}/{values[f'-SP-{i_tab-1}']}")
                        log(hp_sp_total,"HP/SP")
                        if (values[f'-HP_current-{tab_event}']) != "" and values[f'-HP-{tab_event}'] != "":
                            changed_element = list(initiative.keys()).index(selected[int(tab_event)])
                            if float(values[f'-HP_current-{tab_event}']) < float(values[f'-HP-{tab_event}']) // 5:
                                window[f"rec-{changed_element}-name"].update(background_color="red")
                                window[f"rec-{changed_element}-down"].update(background_color="red")
                            elif float(values[f'-HP_current-{tab_event}']) < float(values[f'-HP-{tab_event}']) // 2:
                                window[f"rec-{changed_element}-name"].update(background_color="yellow")
                                window[f"rec-{changed_element}-down"].update(background_color="yellow")
                            elif float(values[f'-HP_current-{tab_event}']) < float(values[f'-HP-{tab_event}']):
                                window[f"rec-{changed_element}-name"].update(background_color="palegreen")
                                window[f"rec-{changed_element}-down"].update(background_color="palegreen")
                            else:
                                window[f"rec-{changed_element}-name"].update(background_color="green")
                                window[f"rec-{changed_element}-down"].update(background_color="green")
                except TypeError as e:
                    pass
                except Exception as e:
                    show_error_popup(str(e))
                    save_values_to_file(values)
            #   #  Если возникает ошибка, выводим сообщение, но приложение продолжает работу
            # show_error_popup(str(e))
            # save_values_to_file(values)
            window.close()
            menu_window.un_hide()
            # except Exception as e:
            # Если возникает ошибка, выводим сообщение, но приложение продолжает работу
            # show_error_popup(str(e))
            if values:
                # print(values['-initiative-'])
                save_values_to_file(values)
    if values:
        # print(values['-initiative-'])
        save_values_to_file(values)
    menu_window.close()
    log("Close")


# Функция обновления данных
def update_rectangles(window, data, selected, values):
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    for index, (key, value) in enumerate(sorted_data):
        # window[f"rec-{index}-init"].update(index)
        window[f"rec-{index}-name"].update(key)
        window[f"rec-{index}-down"].update(str(value))
        tab_event = selected.index(list(data.keys())[int(index)])
        if (values[f'-HP_current-{tab_event}']) != "" and values[f'-HP-{tab_event}'] != "":
            changed_element = index
            if float(values[f'-HP_current-{tab_event}']) < float(values[f'-HP-{tab_event}']) // 5:
                window[f"rec-{changed_element}-name"].update(background_color="red")
                window[f"rec-{changed_element}-down"].update(background_color="red")
            elif float(values[f'-HP_current-{tab_event}']) < float(values[f'-HP-{tab_event}']) // 2:
                window[f"rec-{changed_element}-name"].update(background_color="yellow")
                window[f"rec-{changed_element}-down"].update(background_color="yellow")
            elif float(values[f'-HP_current-{tab_event}']) < float(values[f'-HP-{tab_event}']):
                window[f"rec-{changed_element}-name"].update(background_color="palegreen")
                window[f"rec-{changed_element}-down"].update(background_color="palegreen")
            else:
                window[f"rec-{changed_element}-name"].update(background_color="green")
                window[f"rec-{changed_element}-down"].update(background_color="green")


if __name__ == '__main__':
    main()

# pip install "C:\Users\User\PycharmProjects\Ведьмак\PySimpleGUI-4.60.5-main\PySimpleGUI-4.60.5-main\PySimpleGUI-4.60.5-py3-none-any.whl"
#
