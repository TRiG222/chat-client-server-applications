# Программа сервера
from socket import *
import time
from contextlib import closing
import click


@click.command()
@click.option('--addr', prompt='input ip', help='ip address server', default='')
@click.option('--port', default=8888, prompt='port',
              help='port server.')
def server_answ(addr, port):
    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((addr, port))
        print('Server start')
        s.listen(5)
        while True:
            client, addr = s.accept()
            with closing(client) as cl:
                data = cl.recv(1000000)
                print('Сообщение: ', data.decode('utf-8'), ', было отправлено клиентом: ', addr)
                timestr = time.ctime(time.time()) + "\n"
                print(data.decode('utf-8'))
                if data.decode('utf-8') == 'message1':
                    cl.send('reply1'.encode('utf-8'))
                elif data.decode('utf-8') == 'message2':
                    cl.send('reply2'.encode('utf-8'))
                else:
                    cl.send(timestr.encode('ascii'))


while True:
    server_answ()
