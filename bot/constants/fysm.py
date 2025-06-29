zero_modules = [{'name': 'static', 'name_ru': 'Короткая статика'}, {'name': 'dynamic', 'name_ru': 'Статодинамика'}]

zero_modes = {
    'static': {
        'values': ['4', '6', '8', '12', '14', '16', '18', '20'],
        'weights': [1, 1, 10, 5, 5, 5, 1, 1],
    },
    'dynamic': {
        'values': ['2x8', '2x12', '4x4', '4x8', '4x12', '4x16', '8x4', '8x8'],
        'weights': [5, 5, 5, 10, 8, 1, 1, 1],
    },
}

zero_games = {
    'static': [
        'ON 1',
        'ON 2',
        'ON 3',
        'ON 4',
        'ON 5',
        'ON 6',
        'ON 7',
        'ON 8',
        'ON 9',
        'ON 10',
        'ON 11',
        'ON 12',
        'ON 13',
        'ON 14',
        'ON 15',
        'ON 16',
        'ON 17',
        'ON 18',
    ],
    'dynamic': [
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '10',
        '11',
        '12',
        '13',
        '14',
        '15',
        '16',
        '17',
        '18',
        '19',
        '20',
        '21',
        '22',
        '23',
        '24',
        '25',
        '26',
        '27',
    ],
}

core_practice_modules = {
    'base': {'number_of_games': 1},
    'dense': {'number_of_games': 2},
    'grand': {'number_of_games': 3},
    'mortal': {'number_of_games': 4},
}

core_practice_modes = {
    'values': ['1x2', '1x4', '1x8', '1x18', '2x4', '2x8', '4x2', '4x4'],
    'weights': [3, 5, 10, 2, 4, 3, 3, 3],
}

games = {
    'level_1': {
        'center': [
            'Струна',
            'Детали',
            'Центрирование',
            'Челлендж',
            'Суставной',
            'Завихрение',
            'Экзерсис',
            'Хелз',
            'Хелф',
        ],
        'top': [
            'Азы плотности',
            'Структуризация',
            'Баланс силы',
            'Грань',
            'Интегральный',
            'Уплотнение',
            'Открытие',
            'Железно',
            'Предлог',
        ],
        'bottom': [
            'Корни',
            'Стыковка',
            'Грация',
            'Штиль',
            'Цикличность',
            'Разворот',
            'Компенсация',
            'Мирный воин',
            'Сахар',
        ],
    },
    'level_2': {
        'center': [
            'Ревизия',
            'Устремление',
            'Проработка',
            'Активация центра',
            'Пробуждение силы',
            'Спонтанность',
            'Ошеломляющая безмятежность',
            'Геометрия потока',
            'Однажды',
        ],
        'top': [
            'Стан',
            'Пот',
            'Леер',
            'Лесенка',
            'Вязь',
            'Выход',
            'Раскинуться',
            'Сдвиг',
            'Визит',
        ],
        'bottom': [
            'Платформа',
            'Флюгер',
            'Мягкость',
            'Асимметрия',
            'Классика',
            'Орнамент',
            'Терпение',
            'Вереница',
            'Перелив №1',
        ],
    },
}

games_by_level = {
    'level_1': {
        **games['level_1'],
        'all': [*games['level_1']['center'], *games['level_1']['top'], *games['level_1']['bottom']],
    },
    'level_2': {
        **games['level_2'],
        'all': [*games['level_2']['center'], *games['level_2']['top'], *games['level_2']['bottom']],
    },
    'level_1_and_2': {
        'center': [*games['level_1']['center'], *games['level_2']['center']],
        'top': [*games['level_1']['top'], *games['level_2']['top']],
        'bottom': [*games['level_1']['bottom'], *games['level_2']['bottom']],
        'all': [
            *games['level_1']['center'],
            *games['level_1']['top'],
            *games['level_1']['bottom'],
            *games['level_2']['center'],
            *games['level_2']['top'],
            *games['level_2']['bottom'],
        ],
    },
}
