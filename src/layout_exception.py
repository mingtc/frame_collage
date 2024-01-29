

class LayoutException(Exception):
    """
    custom exception class to to be used in this project just to separate it from the built-in exception classes
    """
    def __init__(self, message):
        super().__init__(message)
