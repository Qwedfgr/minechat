import argparse
import asyncio
import os
from datetime import datetime

import dotenv
from aiofile import AIOFile


async def main():
    dotenv.load_dotenv()
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    history_file = os.getenv('HISTORY')

    while True:
        try:
            reader, writer = await asyncio.open_connection(host=host, port=port)
            while True:
                message_text = (await reader.readline()).decode()
                message_date = datetime.strftime(datetime.now(), '%y.%m.%d %H:%M')
                message = f'[{message_date}] {message_text}'
                async with AIOFile(history_file, 'a') as my_file:
                    await my_file.write(message)
        except ConnectionRefusedError:
            print('Нет соединения. Повторная попытка')
            sleep(3)
            continue


if __name__ == '__main__':
    asyncio.run(main())
