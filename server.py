# Программа сервера
from socket import *
import time

import click


@click.command()
@click.option('--addr', prompt='input ip', help='ip address server', default='')
@click.option('--port', default=8888, prompt='port',
              help='port server.')
def server_answ(addr, port):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((addr, port))
    print('Server start')
    s.listen(5)
    client, addr = s.accept()
    data = client.recv(1000000)
    print('Сообщение: ', data.decode('utf-8'), ', было отправлено клиентом: ', addr)
    timestr = time.ctime(time.time()) + "\n"
    client.send(timestr.encode('ascii'))
    client.close()


while True:
    server_answ()
