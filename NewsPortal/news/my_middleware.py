# Юнит D16.3 Изучение работы middleware
# Представьте, что у вас есть приложение, которое оптимизировано как для ПК,
# так и для мобильных устройств. Шаблоны для этих версий хранятся в каталогах full/ и mobile/.
# Гарантируется, что состав шаблонов идентичен, отличается лишь содержание.
# Создайте простой middleware, который будет отправлять пользователю соответствующую версию.

# Данный MiddleWare не прописан в файле setting, поэтому не работает в данном приложении

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
