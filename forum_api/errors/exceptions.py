class InvalidData(Exception):
    def __init__(self, msg=None, status=400):
        if msg is None:
            msg = "InvalidData"
        super().__init__(msg)
        self.msg = msg
        self.status = status


class NoBody(Exception):
    def __init__(self, msg=None, status=400):
        if msg is None:
            msg = "NoBody"
        super().__init__(msg)
        self.msg = msg
        self.status = status
