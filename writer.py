import argparse
import asyncio
import json
import os

import utils


def get_arguments_parser():
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=formatter_class)
    parser.add_argument('--host', type=str, default=os.getenv('HOST'), help='set host')
    parser.add_argument('--port', type=int, default=os.getenv('PORT_WRITER'), help='set port')
    parser.add_argument('--token', type=str, default=os.getenv('TOKEN'), help='set your token')
    parser.add_argument('--message', type=str, help='write your message')
    parser.add_argument('--nickname', type=str, default=os.getenv('NICKNAME'), help='set your nickname')
    return parser


async def main():
    args = utils.get_args(get_arguments_parser)
    if not args.message:
        return None
    try:
        if not args.nickname:
            args.nickname = input('Укажите ваш ник для регистрации: ')
        nickname = args.nickname.replace('\n', ' ')
        reader, writer = await asyncio.open_connection(host=args.host, port=args.port)
        is_authorized = False
        if args.token:
            is_authorized = await authorise(writer, reader, args.token, nickname)
            if not is_authorized:
                print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        if not is_authorized:
            await register(writer, reader, nickname)
        await submit_message(writer, args.message)
    finally:
        writer.close()


async def register(writer, reader, nickname):
    writer.write(f'{nickname}\n'.encode())
    await writer.drain()
    answer = (await reader.readline()).decode()
    return json.loads(answer)


async def authorise(writer, reader, token, nickname):
    writer.write(f'{token}\n'.encode())
    await reader.readline()
    answer = (await reader.readline()).decode()
    await reader.readline()
    return answer != 'null\n'


async def submit_message(writer, message):
    message = message.replace('\n', ' ')
    writer.write(f'{message}\n\n'.encode())
    await writer.drain()


if __name__ == '__main__':
    asyncio.run(main())
