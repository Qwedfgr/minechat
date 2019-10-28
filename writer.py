import argparse
import asyncio
import os
import logging

import dotenv


def get_arguments_parser():
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=formatter_class)
    parser.add_argument('--host', type=str, default=os.getenv('HOST'), help='set host')
    parser.add_argument('--port', type=int, default=os.getenv('PORT_WRITER'), help='set port')
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

            writer.write(os.getenv('TOKEN').encode())
            writer.write('\n'.encode())
            await writer.drain()
            message = 'gtrhtrhtr\n\n'
            writer.write(message.encode())
            await writer.drain()
            logging.info(message)
            await writer.drain()
        except ConnectionRefusedError:
            print('Нет соединения. Повторная попытка')
            sleep(3)
            continue

if __name__ == '__main__':
    asyncio.run(main())
