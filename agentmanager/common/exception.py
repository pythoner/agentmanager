class Error(Exception):
    pass


class AuthError(Error):
    def __init__(self, msg):
        self.msg = msg


class UpdateError(Error):
    def __init__(self, msg):
        self.msg = msg


class DeleteError(Error):
    def __init__(self, msg):
        self.msg = msg


class SaveError(Error):
    def __init__(self, msg):
        self.msg = msg


class NotFoundError(Error):
    def __init__(self, msg):
        self.msg = msg


class DuplicateError(Error):
    def __init__(self, msg):
        self.msg = msg


class InvalidInputError(Error):
    def __init__(self, msg):
        self.msg = msg


class ForbiddenError(Error):
    def __init__(self, msg):
        self.msg = msg


class ConflictError(Error):
    def __init__(self, msg):
        self.msg = msg


class BadRequestError(Error):
    def __init__(self, msg):
        self.msg = msg
