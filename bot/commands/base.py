from schemas.command import CommandSchema

commands: dict[str, CommandSchema] = {
    "start": CommandSchema(command="start",
                           button_text="Перезапустить бота ♻️"),
    "random": CommandSchema(command="random",
                            button_text="Запустить рандом 🎰"),
}
