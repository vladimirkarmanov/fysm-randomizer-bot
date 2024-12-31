from pydantic import BaseModel


def schema_obj_to_str(obj: BaseModel) -> str:
    fields = '\n'.join([f'{k}: {v}' for k, v in obj.model_dump().items()])
    return f'{obj.__class__.__name__}\n{fields}'
