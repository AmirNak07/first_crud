class EntityNotFoundException(Exception):
    """Исключение, когда сущность не найдена."""

    pass


class EntityAlreadyExistsException(Exception):
    """Исключение, когда сущность уже существует."""

    pass


class BusinessValidationError(Exception):
    """Ошибка бизнес-валидации."""

    pass
