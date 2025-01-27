class BaseLBSException(Exception):
    def __init__(self, message: str, status: int) -> None:
        super(BaseException, self).__init__()
        self.message = message
        self.status = status

    def response(self) -> (str, int):
        return self.message, self.status


class TargetNotExists(BaseLBSException):
    def __init__(self, object_type, object_ids) -> None:
        super(TargetNotExists, self).__init__('Не существуют {} с ID {}'
                                              .format(object_type.__title__, ', '.join([str(x) for x in object_ids])),
                                              404)
        self.object_type = object_type
        self.object_id = object_ids


class MaxOrderExceeded(BaseLBSException):
    def __init__(self, current, maximum) -> None:
        super(MaxOrderExceeded, self).__init__('Превышено максимальное количество заказов: сейчас {} из {}'
                                               .format(current, maximum), 400)
        self.current = current
        self.maximum = maximum


class MaxOrderItemExceed(BaseLBSException):
    def __init__(self, current, maximum) -> None:
        super(MaxOrderItemExceed, self).__init__('Превышено максимальное количество '
                                                 'предметов в заказе: сейчас {} из {}'
                                                 .format(current, maximum), 400)
        self.current = current
        self.maximum = maximum


class IncorrectLunchbox(BaseLBSException):
    def __init__(self) -> None:
        super(IncorrectLunchbox, self).__init__('Данный ланчбокс недоступен для заказа', 400)


class ServiceNotWorking(BaseLBSException):
    def __init__(self) -> None:
        super(ServiceNotWorking, self).__init__('Сервис не работает в текущий день', 400)


class IncorrectTimeslot(BaseLBSException):
    def __init__(self) -> None:
        super(IncorrectTimeslot, self).__init__('Невозможно добавить заказ'
                                                ' с указанным промежутком времени', 400)


class TargetLocked(BaseLBSException):
    def __init__(self, object_type, object_id) -> None:
        super(TargetLocked, self).__init__('{} с ID {} заблокирован'.format(object_type.__title__, object_id), 400)


class TargetArchived(BaseLBSException):
    def __init__(self, object_type, object_id) -> None:
        super(TargetArchived, self).__init__('{} с ID {} архивирован'.format(object_type.__title__, object_id), 400)


class TargetInRelation(BaseLBSException):
    def __init__(self, object_type, ids):
        super(TargetInRelation, self).__init__('{} с ID {} зависят от целевого обьекта!'
                                               .format(object_type.__title__, ', '.join(ids)), 400)


class IncorrectLogin(BaseLBSException):
    def __init__(self):
        super(IncorrectLogin, self).__init__('Неправильные данные для входа!', 400)


class IncorrectPassword(BaseLBSException):
    def __init__(self):
        super(IncorrectPassword, self).__init__('Неправильный пароль для юзера!', 400)


class TargetAlreadyExists(BaseLBSException):
    def __init__(self, object_type):
        super(TargetAlreadyExists, self).__init__('Целевой обьект ({}) уже существует'.format(object_type.__title__),
                                                  400)
