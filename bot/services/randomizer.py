import logging
import random
from dataclasses import dataclass

from constants.fysm import (
    core_practice_modes,
    core_practice_modules,
    games_by_level,
    zero_games,
    zero_modes,
    zero_modules,
)

logger = logging.getLogger(__name__)


@dataclass
class Zero:
    module_name: str
    mode: str
    game: str
    note: str


class RandomizerService:
    def _get_random_zero(self, module_name: str) -> Zero:
        mode = random.choices(
            population=zero_modes[module_name]['values'],
            weights=zero_modes[module_name]['weights'],
            k=1,
        )[0]

        if module_name == 'static':
            game = random.choice(zero_games[module_name])
            game = f'Статика: {game}'
            note = ''
        else:
            games = random.sample(zero_games[module_name], 3)
            game = f'Динамика: {games[0]}, {games[1]}, {games[2]}'
            note = '\n* отдельные упражнения из методички'

        return Zero(
            module_name=module_name,
            mode=mode,
            game=game,
            note=note,
        )

    def _get_random_game_and_mode(
        self,
        fysm_level: str,
        game_type: str,
        excluded_games: list[str],
    ) -> tuple[str, str]:
        games = games_by_level[fysm_level]
        games_by_type = set(games[game_type]) - set(excluded_games)

        game = random.choice(list(games_by_type))
        mode = random.choices(
            population=core_practice_modes['values'],
            weights=core_practice_modes['weights'],
        )[0]
        return game, mode

    def get_full_random_practice(self) -> str:
        zero = self._get_random_zero(random.choice(zero_modules)['name'])

        core_practice = []

        core_module = random.choice(list(core_practice_modules.keys()))
        number_of_games = core_practice_modules[core_module]['number_of_games']

        games_to_exclude: list[str] = []
        for _ in range(number_of_games):
            fysm_level = random.choice(list(games_by_level.keys()))
            games = games_by_level[fysm_level]
            game_type = random.choice(list(games.keys()))

            game, mode = self._get_random_game_and_mode(
                fysm_level,
                game_type,
                excluded_games=games_to_exclude,
            )
            core_practice.append((game, mode))
            games_to_exclude.append(game)

        core_practice_text = '\n'.join([f'{game} - {mode}' for game, mode in core_practice])

        text = (
            f'<b>Включение:</b>\n{zero.game}\n'
            f'Режим: {zero.mode}{zero.note}\n\n'
            f'<b>Основная часть:</b>\n{core_practice_text}'
        )
        return text

    def get_random_practice(
        self,
        zero_module: str,
        first_fysm_level: str,
        first_game_type: str,
        second_fysm_level: str | None = None,
        second_game_type: str | None = None,
        third_fysm_level: str | None = None,
        third_game_type: str | None = None,
        fourth_fysm_level: str | None = None,
        fourth_game_type: str | None = None,
    ) -> str:
        core_practice = {}

        if zero_module == 'random':
            zero_module = random.choice(zero_modules)['name']

        # zero
        zero = self._get_random_zero(zero_module)

        # first game
        game, mode = self._get_random_game_and_mode(first_fysm_level, first_game_type, excluded_games=[])
        core_practice['first'] = {
            'game': game,
            'mode': mode,
        }

        # second game
        if second_fysm_level and second_game_type:
            game, mode = self._get_random_game_and_mode(
                second_fysm_level,
                second_game_type,
                excluded_games=[core_practice['first']['game']],
            )
            core_practice['second'] = {
                'game': game,
                'mode': mode,
            }

        # third game
        if third_fysm_level and third_game_type:
            game, mode = self._get_random_game_and_mode(
                third_fysm_level,
                third_game_type,
                excluded_games=[
                    core_practice['first']['game'],
                    core_practice['second']['game'],
                ],
            )
            core_practice['third'] = {
                'game': game,
                'mode': mode,
            }

        # fourth game
        if fourth_fysm_level and fourth_game_type:
            game, mode = self._get_random_game_and_mode(
                fourth_fysm_level,
                fourth_game_type,
                excluded_games=[
                    core_practice['first']['game'],
                    core_practice['second']['game'],
                    core_practice['third']['game'],
                ],
            )
            core_practice['fourth'] = {
                'game': game,
                'mode': mode,
            }

        core_practice_text = '\n'.join([f'{v["game"]} - {v["mode"]}' for _, v in core_practice.items()])

        text = (
            f'<b>Включение:</b>\n{zero.game}\n'
            f'Режим: {zero.mode}{zero.note}\n\n'
            f'<b>Основная часть:</b>\n{core_practice_text}'
        )
        return text
