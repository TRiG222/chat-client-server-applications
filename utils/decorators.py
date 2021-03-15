import traceback


def log(f):
    def decorator(self, *args, **kwargs):
        self.logger.debug(f'Функция {f.__name__} ({args}, {kwargs}) вызвана из функции '
                          f'{traceback.format_stack()[0].strip().split()[-1]} ')

        return f(self, *args, **kwargs)

    return decorator
