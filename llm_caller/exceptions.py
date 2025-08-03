class OpenAIRequestException(Exception):
    def __init__(self, cause=None):
        self.message = "There was an error with OpenAI."
        self.__cause__ = cause
