from callbacks.fysm import RandomCallback
from constants.fysm import core_practice_modules
from schemas.keyboard import ButtonSchema


def get_zero_module_buttons(callback_name: str) -> list[ButtonSchema]:
    return [
        ButtonSchema(
            text='статика',
            callback_data=RandomCallback(callback_name=callback_name, zero_module='static'),
        ),
        ButtonSchema(
            text='статодинамика',
            callback_data=RandomCallback(callback_name=callback_name, zero_module='dynamic'),
        ),
        ButtonSchema(
            text='доверяю рандому 🔥',
            callback_data=RandomCallback(callback_name=callback_name, zero_module='random'),
        ),
    ]


def get_core_module_buttons(callback_name: str) -> list[ButtonSchema]:
    buttons = []
    for module_name in core_practice_modules.keys():
        buttons.append(
            ButtonSchema(
                text=module_name,
                callback_data=RandomCallback(callback_name=callback_name, core_module=module_name),
            )
        )
    buttons.append(
        ButtonSchema(
            text='доверяю рандому 🔥',
            callback_data=RandomCallback(callback_name=callback_name, core_module='random'),
        )
    )
    return buttons


def get_fysm_level_buttons(callback_name: str) -> list[ButtonSchema]:
    return [
        ButtonSchema(
            text='FYSM 1',
            callback_data=RandomCallback(callback_name=callback_name, fysm_level='level_1'),
        ),
        ButtonSchema(
            text='FYSM 2',
            callback_data=RandomCallback(callback_name=callback_name, fysm_level='level_2'),
        ),
        ButtonSchema(
            text='FYSM 3',
            callback_data=RandomCallback(callback_name=callback_name, fysm_level='level_3'),
        ),
        ButtonSchema(
            text='FYSM 1 + FYSM 2',
            callback_data=RandomCallback(callback_name=callback_name, fysm_level='level_1_and_2'),
        ),
        ButtonSchema(
            text='FYSM 1 + FYSM 3',
            callback_data=RandomCallback(callback_name=callback_name, fysm_level='level_1_and_3'),
        ),
        ButtonSchema(
            text='FYSM 2 + FYSM 3',
            callback_data=RandomCallback(callback_name=callback_name, fysm_level='level_2_and_3'),
        ),
        ButtonSchema(
            text='FYSM 1 + FYSM 2 + FYSM 3',
            callback_data=RandomCallback(callback_name=callback_name, fysm_level='level_1_and_2_and_3'),
        ),
    ]


def get_game_type_buttons(callback_name: str) -> list[ButtonSchema]:
    return [
        ButtonSchema(text='центр', callback_data=RandomCallback(callback_name=callback_name, game_type='center')),
        ButtonSchema(text='верх', callback_data=RandomCallback(callback_name=callback_name, game_type='top')),
        ButtonSchema(text='низ', callback_data=RandomCallback(callback_name=callback_name, game_type='bottom')),
        ButtonSchema(text='все', callback_data=RandomCallback(callback_name=callback_name, game_type='all')),
    ]
