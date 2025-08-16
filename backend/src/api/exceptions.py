class CustomError(Exception):
    default_message = "Unhandled error"

    #
    def __init__(self, message: str | None = None):
        super().__init__(message or self.default_message)


class GameNotFoundError(CustomError):
    default_message = "game not found"


class NotAllPlayersJoinedError(CustomError):
    default_message = "not all players joined"


class GameFinishedError(CustomError):
    default_message = "game finished"


class MoveNotValidError(CustomError):
    default_message = "move not valid"


class WrongPlayerToMoveError(CustomError):
    default_message = "wrong player to move"
