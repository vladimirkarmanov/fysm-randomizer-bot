from typing import Any, Literal


def get_page(current: int, items: dict[int, Any], page_type: Literal['next', 'prev'], infinity: bool = False) -> dict:
    if page_type == 'next':
        if next := items.get(current + 1):
            return next

        if infinity:
            key = list(items.keys())[0]
            return items.get(key)
    elif page_type == 'prev':
        if prev := items.get(current - 1):
            return prev

        if infinity:
            key = list(items.keys())[-1]
            return items.get(key)
    else:
        return items.get(current)

    return items.get(current)
