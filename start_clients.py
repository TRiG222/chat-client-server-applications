import os
from multiprocessing import Pool


def run_process(process):
    print('RUN > python3 {}'.format(process))
    os.system('python3 {}'.format(process))


if __name__ == '__main__':
    with Pool(processes=4) as pool:
        pool.map(run_process, (
            'client.py --id=client1',
            'client.py --id=client2',
            'client.py --id=client3',

        ))
