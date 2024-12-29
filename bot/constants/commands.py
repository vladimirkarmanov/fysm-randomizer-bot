from schemas.command import CommandSchema

side_menu: dict[str, CommandSchema] = {
    'start': CommandSchema(command='start', button_text='Перезапустить бота ♻️ '),
    'random': CommandSchema(command='random', button_text='Запустить рандом 🎰'),
}


menu: dict[str, CommandSchema] = {
    'random': CommandSchema(command='random', button_text='Рандом'),
}
