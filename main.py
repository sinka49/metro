import asyncio
import time

from async_parse_strategy_controller import AsyncParseStrategyController


async def main():
    start_time = time.time()
    controller = AsyncParseStrategyController()
    await controller.start_parsing()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Парсинг завершен за {elapsed_time:.2f} секунд. Получено {controller.count_products} продуктов.")


asyncio.run(main())
