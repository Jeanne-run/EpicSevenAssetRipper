class OperationAbortedByUser(Exception):
    def __init__(self, msg=''):
        self.msg=msg

class NotDataPackZip(Exception):
    def __init__(self, msg):
        self.msg=msg
