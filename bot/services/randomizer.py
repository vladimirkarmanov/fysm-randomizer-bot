import logging
import random
from dataclasses import dataclass

from constants.fysm import core_practice_modes, core_practice_modules, games, zero_games, zero_modes, zero_modules

logger = logging.getLogger(__name__)


@dataclass
class Zero:
    module_name: str
    mode: str
    game: str


class RandomizerService:
    def _get_random_zero(self, module_name: str) -> Zero:
        mode = random.choices(
            population=zero_modes[module_name]['values'],
            weights=zero_modes[module_name]['weights'],
            k=1,
        )[0]
        game = random.choice(zero_games[module_name])

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
            zero_module = random.choice(zero_modules)['name']

        if core_module == 'random':
            core_module = random.choice(list(core_practice_modules.keys()))

        number_of_games = core_practice_modules[core_module]['number_of_games']
        games_for_practice = random.sample(games[fysm_level], number_of_games)
        zero = self._get_random_zero(zero_module)

        modes_for_practice = random.choices(
            population=core_practice_modes['values'],
            weights=core_practice_modes['weights'],
            k=number_of_games,
        )

        core_practice = ''
        for game, mode in zip(games_for_practice, modes_for_practice):
            core_practice += f'{game} - {mode}\n'

        text = f'<b>Включение:</b>\n{zero.game} - {zero.mode}\n\n' f'<b>Основная часть:</b>\n{core_practice}'
        return text
