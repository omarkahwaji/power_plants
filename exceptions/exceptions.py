class DataNotFoundExceptionError(Exception):
    def __init__(self, message: str):
        self.message = message

class BadMetricError(Exception):
    def __init__(self, message: str):
        self.message = message
