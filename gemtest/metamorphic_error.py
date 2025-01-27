import abc


class MetamorphicRelationError(Exception, metaclass=abc.ABCMeta):
    def __init__(self, message, original_exception: Exception = None):
        self.message = message
        self.original_exception = original_exception


class SUTExecutionError(MetamorphicRelationError):
    pass


class TransformationError(MetamorphicRelationError):
    pass


class RelationError(MetamorphicRelationError):
    pass


class InvalidInputError(MetamorphicRelationError):
    pass


class SkippedMTC(MetamorphicRelationError):
    pass


def skip(message: str):
    raise SkippedMTC(message)
