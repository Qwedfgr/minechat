import argparse
import asyncio
import os
from datetime import datetime
import logging


import dotenv
from aiofile import AIOFile


def get_arguments_parser():
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=formatter_class)
    parser.add_argument('--host', type=str, default=os.getenv('HOST'), help='set host')
    parser.add_argument('--port', type=int, default=os.getenv('PORT_READER'), help='set port')
    parser.add_argument('--history', type=str, default=os.getenv('HISTORY'), help='set path to history file')
    return parser


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s: %(message)s',
        datefmt='%H:%M:%S',
    )

    dotenv.load_dotenv()
    parser = get_arguments_parser()
    args = parser.parse_args()

    while True:
        try:
            reader, writer = await asyncio.open_connection(host=args.host, port=args.port)
            while True:
                message_text = (await reader.readline()).decode()
                message_date = datetime.strftime(datetime.now(), '%y.%m.%d %H:%M')
                message = f'[{message_date}] {message_text}'
                logging.info(message)
                async with AIOFile(args.history, 'a') as my_file:
                    await my_file.write(message)
        except ConnectionRefusedError:
            print('Нет соединения. Повторная попытка')
            sleep(3)
            continue


if __name__ == '__main__':
    asyncio.run(main())
