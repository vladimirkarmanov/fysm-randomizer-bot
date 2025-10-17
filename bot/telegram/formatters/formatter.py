from dataclasses import fields


def entity_to_str(entity) -> str:
    result = '\n'.join([f'{field.name}: {getattr(entity, field.name)}' for field in fields(entity)])
    return f'{entity.__class__.__name__}\n{result}'
