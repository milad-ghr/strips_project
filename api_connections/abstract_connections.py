

class AbstractConnection:
    DEFAULT_API_ENDPOINT = None

    def __init__(self, user= None, *args, **kwargs):
        if user:
            self.user = user
        else:
            self.user = None

    def _request_api(self, method: str, data: dict, endpoint: str):
        raise NotImplementedError()

    def create_payment_method(self, *args, **kwargs):
        raise NotImplementedError()

    def update_payment_method(self, *args, **kwargs):
        raise NotImplementedError()

    def delete_payment_method(self, *args, **kwargs):
        pass

    def create_customer(self, *args, **kwargs):
        raise NotImplementedError()

    def update_customer(self, *args, **kwargs):
        pass

    def delete_customer(self, *args, **kwargs):
        pass

    def create_subscription(self, *args, **kwargs):
        raise NotImplementedError()

    def update_subscription(self, *args, **kwargs):
        pass


