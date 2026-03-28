from random import randint, choice
from Custom_scripts import *
import PySimpleGUI as sg

loaded_data = load_lists_json("witcher_game_data.json",)
cprint = sg.cprint

def roll_d6():
    r = randint(1, 6)
    log(r,"ROLL D6")
    print(r)
    cprint(r)
    return r


def roll_d10(indicate=True):
    r = randint(1, 10)
    log(r,"ROLL D10")
    if indicate:
        print(r)
        cprint(r)
    return r


def roll_d100():
    return (roll_d10() - 1) * 10 + roll_d10()


def special_d10_roll():
    """
    Особый бросок d10:
    - Если выпало 10, продолжаем добавлять броски, пока не выпадет другое число.
    - Если выпала 1, продолжаем вычитать броски, пока не выпадет другое число.
    - Все остальные числа возвращаются как есть.
    """
    roll = roll_d10()
    result = 0

    if roll == 10:
        # Суммируем все броски, пока выпадает 10
        while roll == 10:
            result += roll
            roll = roll_d10()
        result += roll  # Добавляем последний бросок
    elif roll == 1:
        # Вычитаем все броски, пока выпадает 1
        roll = roll_d10()
        while roll == 10:
            result -= roll
            roll = roll_d10()
        result -= roll  # Вычитаем последний бросок
    else:
        # Обычный результат
        result = roll

    cprint(f"--")
    return result


def crit_damage(attack, defense, body_part, window, tab_event):
    injuries = {
        "Смертельная травма": {'Голова': ("Сломанная шея", "Повреждение глаза")[randint(0, 1)],
                               'Тело': ("Травма сердца", "Септический шок")[randint(0, 1)],
                               'П.Р.': "Потеря п. руки", 'Л.Р.': "Потеря л. руки", 'П.Н.': "Потеря п. ноги",
                               'Л.Н.': "Потеря л. ноги"},
        "Тяжелая травма": {'Голова': ("Проломленный череп", "Контузия")[randint(0, 1)],
                           'Тело': ("Рана в живот", "Сосущая рана грудной клетки")[randint(0, 1)],
                           'П.Р.': "Открытый перелом п. руки", 'Л.Р.': "Открытый перелом л. руки",
                           'П.Н.': "Открытый перелом ноги", 'Л.Н.': "Открытый перелом л. ноги"},
        "Средняя травма": {'Голова': ("Небольшая травма головы", "Выбитые зубы")[randint(0, 1)],
                           'Тело': ("Разрыв селезёнки", "Сломанные рёбра")[randint(0, 1)], 'П.Р.': "Перелом п. руки",
                           'Л.Р.': "Перелом руки", 'П.Н.': "Перелом п. ноги", 'Л.Н.': "Перелом л. ноги"},
        "Лёгкая травма": {'Голова': ("Треснувшая челюсть", "Уродующий шрам")[randint(0, 1)],
                          'Тело': ("Треснувшие рёбра", "Инородный объект")[randint(0, 1)], 'П.Р.': "Вывих п. руки",
                          'Л.Р.': "Вывих руки", 'П.Н.': "Вывих п. ноги", 'Л.Н.': "Вывих л. ноги"},
    }

    damage_levels = [(15, "Смертельная травма", 10),
                     (13, "Тяжелая травма", 8),
                     (10, "Средняя травма", 5),
                     (7, "Лёгкая травма", 3)]

    for threshold, injury_type, damage in damage_levels:
        if attack - defense >= threshold:
            window[f'-OUTPUT-{tab_event}'].update(f"{injury_type}: {injuries[injury_type][body_part]}\n", append=True)
            return damage
    return 0


def random_name(sex, race):
    # if race == ["Муж", "Жен", "Люб"], ["Люди", "Aen Seidhe", "Крас", "Люб"]
    # print(sex,race)
    names = {
        ("Муж", "Север"): loaded_data["human_male_names"],
        ("Муж", "Туссент"): loaded_data["toussaint_male_names"],
        ('Муж', 'Aen Seidhe'): loaded_data["elf_male_names"],
        ('Муж', 'Краснолюд'): loaded_data["dwarf_male_names"],
        ('Муж', 'Низушек'): loaded_data["halfling_male_names"],
        ('Муж', 'Гном'): loaded_data["gnome_male_names"],
        ('Муж',
         'Люб'): loaded_data["human_male_names"] + loaded_data["elf_male_names"] + loaded_data["dwarf_male_names"] + loaded_data["toussaint_male_names"] + loaded_data["halfling_male_names"] + loaded_data["gnome_male_names"],
        ("Жен", "Север"): loaded_data["human_female_names"],
        ("Жен", "Низушек"): loaded_data["halfling_female_names"],
        ("Жен", "Гном"): loaded_data["gnome_female_names"],
        ("Жен", "Туссент"): loaded_data["toussaint_female_names"],
        ('Жен', 'Aen Seidhe'): loaded_data["elf_female_names"],
        ('Жен', 'Краснолюд'): loaded_data["dwarf_female_names"],
        ('Жен',
         'Люб'): loaded_data["human_female_names"] + loaded_data["elf_female_names"] + loaded_data["dwarf_female_names"] + loaded_data["toussaint_female_names"] + loaded_data["gnome_female_names"] + loaded_data["halfling_female_names"],
        ("Люб", "Туссент"): loaded_data["toussaint_male_names"] + loaded_data["toussaint_female_names"],
        ("Люб", "Север"): loaded_data["human_male_names"] + loaded_data["human_female_names"],
        ('Люб', 'Aen Seidhe'): loaded_data["elf_male_names"] + loaded_data["elf_female_names"],
        ('Люб', 'Краснолюд'): loaded_data["dwarf_male_names"] + loaded_data["dwarf_female_names"],
        ('Люб', 'Низушек'): loaded_data["halfling_male_names"] + loaded_data["halfling_female_names"],
        ('Люб', 'Гном'): loaded_data["gnome_male_names"] + loaded_data["gnome_female_names"],
        ('Люб',
         'Люб'): loaded_data["human_male_names"] + loaded_data["elf_male_names"] + loaded_data["dwarf_male_names"] + loaded_data["human_female_names"] + loaded_data["elf_female_names"] + loaded_data["dwarf_female_names"] + loaded_data["toussaint_male_names"] + loaded_data["toussaint_female_names"] + loaded_data["gnome_female_names"] + loaded_data["halfling_female_names"] + loaded_data["halfling_male_names"] + loaded_data["gnome_male_names"],
    }[(sex, race)]

    return f'{choice(names)} "{choice(loaded_data["nicknames"])}"'


def random_things(rarity="Обычные"):
    global personal_items
    # import inspect
    # print(inspect.currentframe().f_back.f_globals)
    return personal_items[loaded_data["personal_items_types"].index(rarity)][roll_d100()]


def generate_character_description():
    # Расширенная таблица (15 столбцов)
    # Получаем результаты из таблицы по независимым броскам
    race, gender, age, character, history, status, romance, secret, clothing, hairstyle, hair_color,  eye_color, accessories, personality, values_who, values_what, attitude = (
        loaded_data["character_table"][0][roll_d10() - 1],
        loaded_data["character_table"][1][roll_d10() - 1],
        loaded_data["character_table"][2][roll_d10() - 1],
        loaded_data["character_table"][3][roll_d10() - 1],
        loaded_data["character_table"][4][roll_d10() - 1],
        loaded_data["character_table"][5][roll_d10() - 1],
        loaded_data["character_table"][6][roll_d10() - 1],
        loaded_data["character_table"][7][roll_d10() - 1],
        loaded_data["character_table"][8][roll_d10() - 1],
        loaded_data["character_table"][9][roll_d10() - 1],
        loaded_data["character_table"][10][roll_d10() - 1],
        loaded_data["character_table"][11][roll_d10() - 1],
        loaded_data["character_table"][12][roll_d10() - 1],
        loaded_data["character_table"][13][roll_d10() - 1],
        loaded_data["character_table"][14][roll_d10() - 1],
        loaded_data["character_table"][15][roll_d10() - 1],
        loaded_data["character_table"][16][roll_d10() - 1],
    )

    name_var = " / ".join(
        [random_name(gender.title()[:3], ["Север", "Туссент"][randint(0, 1)] if race == "Человек" else race) for _ in
         range(3)])
    # Формируем описательное предложение
    description = (f"Варианты имён: {name_var}"
                   "\n"
                   f"{race} {gender.lower()} {age.lower()}. "
                   f"Внешность: {clothing.lower()}, {hairstyle.lower()}, {hair_color.lower()}, {eye_color.lower()}, {accessories.lower()}. "
                   f"Положение: {status.lower()}. {history}. "
                   "\n"
                   f"Характер: {character.lower()}/{personality.lower()}. "
                   f"Ценности: ценит {values_who.lower()}, выше всего ставит {values_what.lower()}. "
                   f"Отношение к другим: {attitude.lower()}."
                   "\n"
                   f"{'Нет романтических отношений. ' if romance == 'Нет' else f'Роман: {romance.lower()}. '}"
                   f"Тайна: {secret.lower()}."
                   )

    return description


def generate_scoiatael():
    # Итоговая таблица для Скоя'таэлей (8 столбцов)

    # Получаем результаты по независимым броскам
    race, gender, physical1, physical2, equipment1, equipment2, behavior1, behavior2, motivation1, motivation2, secret1, secret2 = (
        loaded_data["scoiatael_table"][0][roll_d10() - 1],
        loaded_data["scoiatael_table"][1][roll_d10() - 1],
        loaded_data["scoiatael_table"][2][roll_d10() - 1],
        loaded_data["scoiatael_table"][3][roll_d10() - 1],
        loaded_data["scoiatael_table"][4][roll_d10() - 1],
        loaded_data["scoiatael_table"][5][roll_d10() - 1],
        loaded_data["scoiatael_table"][6][roll_d10() - 1],
        loaded_data["scoiatael_table"][7][roll_d10() - 1],
        loaded_data["scoiatael_table"][8][roll_d10() - 1],
        loaded_data["scoiatael_table"][9][roll_d10() - 1],
        loaded_data["scoiatael_table"][10][roll_d10() - 1],
        loaded_data["scoiatael_table"][11][roll_d10() - 1],
    )
    print(race, gender, physical1, physical2, equipment1, equipment2, behavior1, behavior2, motivation1, motivation2, secret1, secret2)
    name_var = " / ".join(
        [random_name(gender.title()[:3], ["Север", "Туссент"][randint(0, 1)] if race == "Человек" else race) for _ in
         range(3)])
    # Формируем описательное предложение
    description = (f"Варианты имён: {name_var}"
                   "\n"
                   f"{race} {gender.lower()}. "
                   f"Внешность: {[physical1.lower(), physical2.lower()][randint(0, 1)]}. "
                   f"Снаряжение: {[equipment1.lower(), equipment2.lower()][randint(0, 1)]}. "
                   "\n"
                   f"Поведение: {[behavior1.lower(), behavior2.lower()][randint(0, 1)]}. "
                   f"Мотивация быть Белкой: {[motivation1.lower(), motivation2.lower()][randint(0, 1)]}"
                   )

    return description


def reserv():
    stats = {"ИНТЕЛЛЕКТ": 1,
             "РЕАКЦИЯ": 1,
             "ЛОВКОСТЬ": 1,
             "ТЕЛОСЛОЖЕНИЕ": 1,
             "СКОРОСТЬ": 1,
             "ЭМПАТИЯ": 1,
             "РЕМЕСЛО": 1,
             "ВОЛЯ": 1}
    added_stats = {
        # "ПЗ": stats["ТЕЛОСЛОЖЕНИЕ"] * 5,
        # "ВЫН": stats["ТЕЛОСЛОЖЕНИЕ"] * 5,
        "ПЗ": round((stats["ТЕЛОСЛОЖЕНИЕ"] + stats["ВОЛЯ"]) // 2) * 5,
        "ВЫН": round((stats["ТЕЛОСЛОЖЕНИЕ"] + stats["ВОЛЯ"]) // 2) * 5,
        "Бег": stats["СКОРОСТЬ"] * 3,
        "Отдых": stats["ТЕЛОСЛОЖЕНИЕ"],
        "Уст": stats["ТЕЛОСЛОЖЕНИЕ"],
        "Энергия": 0,
    }

    skills = {
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
    #       ['Голова', 'Тело', 'П.Р.', 'Л.Р.', 'П.Н.', 'Л.Н.']
    armor = [0, 0, 0, 0, 0, 0]
    weapon = [
        ['Когти', (5, 0), 'Нет', 0, 2], ['Укус', (6, 0), 'Кровопускающее (50%)', 0, 1],
        ['Нож', (1, 2), '', 0, 1],
        ['Нога', [(1, 0), (1, 2), (1, 4), (1, 6), (1, 8), (1, 10), (1, 12)][stats["ТЕЛОСЛОЖЕНИЕ"] // 2],
         'Несмертельный', 0,
         1],
        ['Рука', [(1, -4), (1, -2), (1, 0), (1, 2), (1, 4), (1, 6), (1, 8)][stats["ТЕЛОСЛОЖЕНИЕ"] // 2],
         'Несмертельный ',
         0, 1],
    ]
    mining = [""]
    abilities = [""]
    description = [""]
    weakness = [""]
    difficult = [""]
    type = "_Неизвестно"
    name = 'Никто'

    with open("C:/Users/User/PycharmProjects/Ведьмак/.temp/temp", "a", encoding="utf-8") as f:
        f.write(str((stats, added_stats, skills, armor, name, weapon, mining, abilities, weakness, description,
                     difficult, type)) + "\n")


if __name__ == '__main__':
    all_game_data = {
        "human_male_names": human_male_names,
        "human_female_names": human_female_names,
        "dwarf_male_names": dwarf_male_names,
        "dwarf_female_names": dwarf_female_names,
        "elf_male_names": elf_male_names,
        "elf_female_names": elf_female_names,
        "toussaint_male_names": toussaint_male_names,
        "toussaint_female_names": toussaint_female_names,
        "halfling_male_names": halfling_male_names,
        "halfling_female_names": halfling_female_names,
        "gnome_male_names": gnome_male_names,
        "gnome_female_names": gnome_female_names,
        "personal_items_types": personal_items_types,
        "personal_items": personal_items,
        "character_table": character_table,
        "scoiatael_table": scoiatael_table,
        "race_features_data": race_features_data,
        "race_features_headings": race_features_headings,

    }
    with open('witcher_game_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_game_data, f, ensure_ascii=False, indent=2)

    print("Все данные сохранены в witcher_app_data.json")
    # r = personal_items[0]
    # print(len(r))
    # print("[")
    # for i in r:
    #     print(f'"{i}",')
    # print("]")
    # print(len(r))
