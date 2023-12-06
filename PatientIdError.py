
class PatientIdError(Exception):
    def __init__(self, index_error=None, value_error=None):
        self.index_error = index_error
        self.value_error = value_error
