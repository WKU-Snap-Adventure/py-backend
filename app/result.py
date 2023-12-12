class Result:
    CODE_SUCCESS = 200
    CODE_FAIL = -1

    def __init__(self):
        self.code = ''
        self.message = ''
        self.data = None

    def success(self, data=None):
        self.code = self.CODE_SUCCESS
        self.message = 'success'
        self.data = data
        return self

    def fail(self, message='fail'):
        self.code = self.CODE_FAIL
        self.message = message
        return self
