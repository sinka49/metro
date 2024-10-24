from datetime import datetime
from typing import List
import aiofiles
from aiocsv import AsyncWriter

from constants import SRC_FOR_WRITE, FILE_FOR_WRITE


class AsyncCsvWriter:
    def __init__(self) -> None:
        """
        Инициализация объекта AsyncCsvWriter
        """
        self.src: str = f"{SRC_FOR_WRITE}{str(datetime.now())}{FILE_FOR_WRITE}"

    async def write_to_csv(self, data: List[dict]) -> None:
        """
        Метод для записи в файл
        """
        async with aiofiles.open(self.src, 'a', newline='') as f:
            writer = AsyncWriter(f)
            new_data = [list(product.values()) for product in data]
            await writer.writerows(new_data)
