from services.base import BaseService
from random import choice, sample
from dataclasses import dataclass

from constants.fysm import (
    zero_modules,
    zero_modes,
    core_practice_modules,
    games,
    core_practice_modes,
    zero_games,
    hard_zero_modes,
    normal_core_practice_modes,
)


@dataclass
class Zero:
    module_name: str
    mode: str
    game: str


class RandomizerService(BaseService):

    def _get_random_zero(self) -> Zero:
        module_name = choice(zero_modules)['name']
        mode = choice(zero_modes[module_name])
        game = choice(zero_games[module_name])

        return Zero(
            module_name=module_name,
            mode=mode,
            game=game,
        )

    def get_random_practice(
        self,
        core_module_name: str,
        fysm_level: str,
    ) -> str:
        zero = self._get_random_zero()

        if core_module_name == 'random':
            core_module_name = choice(list(core_practice_modules.keys()))

        number_of_games = core_practice_modules[core_module_name]['number_of_games']

        games_for_practice = sample(games[fysm_level], number_of_games)

        if zero.mode in hard_zero_modes[zero.module_name]:
            modes_for_practice = [choice(normal_core_practice_modes) for _ in range(number_of_games)]
        else:
            modes_for_practice = [choice(core_practice_modes) for _ in range(number_of_games)]

        core_practice = ''
        for game, mode in zip(games_for_practice, modes_for_practice):
            core_practice += f'{game} - {mode}\n'

        text = (f'<b>Включение:</b>\n{zero.game} - {zero.mode}\n\n'
                f'<b>Основная часть:</b>\n{core_practice}')
        return text


randomizer_service = RandomizerService()
