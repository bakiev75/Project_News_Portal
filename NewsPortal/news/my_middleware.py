# Юнит D16.3 Изучение работы middleware
# Представьте, что у вас есть приложение, которое оптимизировано как для ПК,
# так и для мобильных устройств. Шаблоны для этих версий хранятся в каталогах full/ и mobile/.
# Гарантируется, что состав шаблонов идентичен, отличается лишь содержание.
# Создайте простой middleware, который будет отправлять пользователю соответствующую версию.

# Данный MiddleWare не прописан в файле setting, поэтому не работает в данном приложении. Приведен в качестве примера

class MobileOrFullMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.mobile:
            prefix = "mobile/"
        else:
            prefix = "full/"
        response.template_name = prefix + response.template_name
        return response


import pytz

from django.utils import timezone

# Данный MiddleWare для обработки часовых поясов

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')  # пытаемся забрать часовой пояс из сессии
        #  если он есть в сессии, то выставляем такой часовой пояс. Если же его нет, значит он не установлен, и часовой пояс надо выставить по умолчанию (на время сервера)
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
