import functools

from flask import request, jsonify

from theater.helper.code import Code


class Validator():
    def __init__(self, **params_template):
        self.pt = params_template

    # the objects of the instantiation of class can be called as function
    def __call__(self, func):
        # without the 'functools.wraps', the name of the decorated function will change to the function name of the decorator,
        # and cannot call the '__doc__'
        @functools.wraps(func)
        # the parameters come from the decorated function
        def decorated_function(*args, **kwargs):
            try:
                # create the customized parameter directory
                request.params = {}
                for p in self.pt:
                    request.params[p] = self.pt[p](request.values[p])
            except Exception:
                # return the status
                # traceback.print_exc()
                response = jsonify(
                    rc=Code.required_parameter_missing.value,
                    msg=Code.required_parameter_missing.name,
                    data={'required_param': p}
                )
                response.status_code = 400
                return response
            # successfully call the decorated function, 'func' comes from the 'call' function
            return func(*args, **kwargs)

        return decorated_function


class ValidationError(Exception):
    def __int__(self, message, values):
        super(ValidationError, self).__int__(message)
        self.values = values


def digit(value, can_be_empty=False):
    if can_be_empty and not str(value).isdigit():
        raise ValidationError('Digit value must be digit:%s' % value)
    return value


def multi_int(values, sperator=',', can_be_empty=False):
    if can_be_empty and not values:
        return []
    return [int(i) for i in values.split(sperator)]


def complex_int(value, length=0, sperator='-'):
    digits = value.split(sperator)
    if not digits or (length != 0 and len(digits) != length):
        raise ValidationError('complex int error:%s' % value, value)
    result = []
    for digit in digits:
        if not digit.isdigit():
            raise ValidationError('complex int error:%s' % value, value)
        result.append(int(digit))
    return tuple(result)


def multi_complex_int(values, sperator=',', can_be_empty=False):
    if can_be_empty and not values:
        return []
    return [complex_int(i) for i in values.split(sperator)]
