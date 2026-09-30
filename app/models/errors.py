class NumericalError(Exception):
    pass


class ValidationError(NumericalError):
    pass


class EvaluationError(NumericalError):
    pass
