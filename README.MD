# Чат

Скрипт для чтения и отправки сообщений из командной строки.

## Как установить

Для работы нужен Python версии не ниже 3.7.


```bash
pip install -r requirements.txt
```

## Как запустить
Пример установки переменных окружения можно посмотреть в файле ```env_example```
```.env
HOST=minechat.dvmn.org
PORT_READER=5000
PORT_WRITER=5050
NICKNAME=default nick
HISTORY=history.txt
TOKEN=TOKEN
```
Для запуска скрипта для чтения и логирования чата:
```bash
python reader.py
```
Для получения дополнительной информации об аргументах:
```bash
python reader.py --help
```

```bash
usage: reader.py [-h] [--host HOST] [--port PORT] [--history HISTORY]

optional arguments:
  -h, --help         show this help message and exit
  --host HOST        set host (default: minechat.dvmn.org)
  --port PORT        set port (default: 5000)
  --history HISTORY  set path to history file (default: history.txt)
```

Для запуска скрипта для отправки сообщений:
```bash
python writer.py --message text
```
Для получения дополнительной информации об аргументах:
```bash
python writer.py --help
```

```bash
usage: writer.py [-h] [--host HOST] [--port PORT] [--token TOKEN]
                 [--message MESSAGE] [--nickname NICKNAME]

optional arguments:
  -h, --help           show this help message and exit
  --host HOST          set host (default: minechat.dvmn.org)
  --port PORT          set port (default: 5050)
  --token TOKEN        set your token (default: token)
  --message MESSAGE    write your message (default: None)
  --nickname NICKNAME  set your nickname (default: default nick)
```