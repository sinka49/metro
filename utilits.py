from typing import Optional
from constants import BASE_URL, URL_PARAMS, PAGE


def get_url(category, page: Optional[int] = None) -> str:
    return f"{BASE_URL}{category}{URL_PARAMS}{PAGE}{str(page)}" if page else f"{BASE_URL}{category}{URL_PARAMS}"
