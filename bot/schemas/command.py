from pydantic import BaseModel


class CommandSchema(BaseModel):
    command: str
    button_text: str

    @property
    def telegram_command(self):
        return f"/{self.command}"
