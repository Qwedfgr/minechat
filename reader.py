import argparse
import asyncio
import logging
import os
from datetime import datetime

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
    utils.logging_config()
    args = utils.get_args(get_arguments_parser)
    attempt = 0
    reader, writer = await asyncio.open_connection(host=args.host, port=args.port)
    while True:
        try:
            if attempt:
                logging.info('Установлено соединение')
                attempt = 0
            message = await get_message_text(reader)
            logging.info(message)
            async with AIOFile(args.history, 'a') as my_file:
                await my_file.write(message)
        except (ConnectionResetError, ConnectionRefusedError):
            attempt += 1
            if attempt < 3:
                logging.info('Нет соединения. Повторная попытка')
            else:
                logging.info('Нет соединения. Повторная попытка через 3 сек.')
                await asyncio.sleep(3)
                continue


async def get_message_text(reader):
    message_text = (await reader.readline()).decode()
    message_date = datetime.strftime(datetime.now(), '%y.%m.%d %H:%M')
    message = f'[{message_date}] {message_text}'
    return message


if __name__ == '__main__':
    asyncio.run(main())
