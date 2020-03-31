

class BaseDriver(object):
    def __init__(self, exit_code = 0):
        self.exit_code_ = exit_code

    @property
    def ExitCode(self):
        return self.exit_code_
