from core.deps import get_settings

settings = get_settings()

zero_modules = [
    {
        'name': 'static',
        'name_ru': 'Короткая статика'
    },
    {
        'name': 'dynamic',
        'name_ru': 'Статодинамика'
    }
]

zero_modes = {
    'static': [
        '8', '12', '16', '20', '24'
    ],
    'dynamic': [
        '4x8', '4x12', '4x16', '8x4', '8x8', '8x12'
    ]
}

zero_games = {
    'static': [
        'ON 1', 'ON 2', 'ON 3', 'ON 4', 'ON 5'
    ],
    'dynamic': [
        'ZERO 1', 'ZERO 2', 'ZERO 3', 'ZERO 4', 'ZERO 5', 'ZERO 6', 'ZERO 7', 'ZERO 8', 'ZERO 9'
    ]
}

hard_zero_modes = {
    'static': ['16', '20', '24'],
    'dynamic': ['4x16', '8x8', '8x12'],
}

core_practice_modules = {
    'base': {
        'number_of_games': 1
    },
    'dense': {
        'number_of_games': 2
    },
    'grand': {
        'number_of_games': 3
    },
    'mortal': {
        'number_of_games': 4
    },
}

core_practice_modes = [
    '1x8', '1x18', '2x4', '2x8', '4x2', '4x4'
]

normal_core_practice_modes = ['1x8', '2x4', '4x2']

games_by_level = {
    'level_1': [
        'Струна',
        'Почувствуй детали',
        'Центрирование',
        'Челлендж',
        'Суставной тренаж',
        'Завихрение',
        'Спинные экзерсисы',
        'Мэнс хелз',
        'Вумэнс хелз',
    ],
    'level_1_episodes': [
        'Азы плотности',
        'Структуризация',
        'Баланс и сила',
        'Грань',
        'Интегральный',
        'Уплотнение',
        'Открытие',
        'Железно',
        'Корни',
        'Стыковка',
        'Грация',
        'Штиль',
        'Цикличность',
        'Разворот',
        'Компенсация',
        'Мирный воин',
    ],
    'level_2': [
        'Ревизия',
        'Устремление',
        'Проработка',
        'Активация центра',
        'Пробуждение силы',
        'Спонтанность',
        'Ошеломляющая безмятежность',
        'Геометрия потока',
        'Однажды',
    ]
}

games = {
    'level_1': games_by_level['level_1'],
    'level_1_episodes': [*games_by_level['level_1'], *games_by_level['level_1_episodes']],
    'level_2': [*games_by_level['level_1'], *games_by_level['level_1_episodes'], *games_by_level['level_2']],
}
