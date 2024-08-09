from dataclasses import dataclass
from random import choice, sample

from constants.fysm import (
    core_practice_modes,
    core_practice_modules,
    games,
    hard_zero_modes,
    normal_core_practice_modes,
    zero_games,
    zero_modes,
    zero_modules,
)
from services.base import BaseService


@dataclass
class Zero:
    module_name: str
    mode: str
    game: str


class RandomizerService(BaseService):

    def _get_random_zero(self, module_name: str) -> Zero:
        mode = choice(zero_modes[module_name])
        game = choice(zero_games[module_name])

        return Zero(
            module_name=module_name,
            mode=mode,
            game=game,
        )

    def get_random_practice(
        self,
        zero_module: str,
        fysm_level: str,
        core_module: str,
    ) -> str:
        if zero_module == 'random':
            zero_module = choice(zero_modules)['name']

        if core_module == 'random':
            core_module = choice(list(core_practice_modules.keys()))

        number_of_games = core_practice_modules[core_module]['number_of_games']
        games_for_practice = sample(games[fysm_level], number_of_games)
        zero = self._get_random_zero(zero_module)

        if zero.mode in hard_zero_modes[zero.module_name]:
            modes_for_practice = [choice(normal_core_practice_modes) for _ in range(number_of_games)]
        else:
            modes_for_practice = [choice(core_practice_modes) for _ in range(number_of_games)]

        core_practice = ''
        for game, mode in zip(games_for_practice, modes_for_practice):
            core_practice += f'{game} - {mode}\n'

        text = f'<b>Включение:</b>\n{zero.game} - {zero.mode}\n\n' f'<b>Основная часть:</b>\n{core_practice}'
        return text


randomizer_service = RandomizerService()
