import argparse
import asyncio
import os
from concurrent.futures import TimeoutError
from datetime import datetime
from socket import gaierror

from aiofile import AIOFile

import utils


def get_arguments_parser():
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=formatter_class)
    parser.add_argument('--host', type=str, default=os.getenv('HOST'), help='set host')
    parser.add_argument('--port', type=int, default=os.getenv('PORT_READER'), help='set port')
    parser.add_argument('--history', type=str, default=os.getenv('HISTORY'), help='set path to history file')
    return parser


async def main():
    args = utils.get_args(get_arguments_parser)
    attempt = 0

    while True:
        try:
            reader, writer = await asyncio.open_connection(host=args.host, port=args.port)
            if attempt:
                print(await write_message_to_file(args.history, 'Установлено соединение\n'))
                attempt = 0
            message = await get_message_text(reader)
            print(await write_message_to_file(args.history, message))
        except (ConnectionRefusedError, ConnectionResetError, gaierror, TimeoutError):
            attempt += 1
            if attempt <= 3:
                error_message = 'Нет соединения. Повторная попытка\n'
                await write_message_to_file(args.history, error_message)
            else:
                error_message = 'Нет соединения. Повторная попытка через 3 сек.\n'
                print(await write_message_to_file(args.history, error_message))
                await asyncio.sleep(3)
                continue
        finally:
            writer.close()


async def get_message_text(reader):
    data = await asyncio.wait_for(reader.readline(), timeout=5)
    message = data.decode()
    return message


async def write_message_to_file(file, message_text):
    async with AIOFile(file, 'a') as my_file:
        message_date = datetime.strftime(datetime.now(), '%y.%m.%d %H:%M')
        message = f'[{message_date}] {message_text}'
        await my_file.write(message)
    return message

if __name__ == '__main__':
    asyncio.run(main())
