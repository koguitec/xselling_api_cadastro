"""Module for structured response objects"""


class ResponseTypes:
    """Class for response types"""

    PARAMETERS_ERROR = 'ParametersError'
    RESOURCE_ERROR = 'ResourceError'
    SYSTEM_ERROR = 'ServerError'
    SUCCESS = 'Success'
    DOMAIN_ERROR = 'DomainAlreadyExistsError'


STATUS_CODE = {
    ResponseTypes.SUCCESS: 200,
    ResponseTypes.RESOURCE_ERROR: 404,
    ResponseTypes.PARAMETERS_ERROR: 400,
    ResponseTypes.SYSTEM_ERROR: 500,
    ResponseTypes.DOMAIN_ERROR: 409,
}


class ResponseFailure:
    """Class for managing response failures"""

    def __init__(self, type_, message):
        self.type = type_
        self.message = self._format_message(message)

    def _format_message(self, msg):
        if isinstance(msg, Exception):
            return '{}: {}'.format(msg.__class__.__name__, '{}'.format(msg))
        return msg

    @property
    def value(self):
        return {'error': {'type': self.type, 'message': self.message}}

    def __bool__(self):
        return False


class ResponseSuccess:
    """Class for managing response success"""

    def __init__(self, value=None, type_: str = None):
        self.type = ResponseTypes.SUCCESS

        if type_:
            self.value = {
                'type': type_,
                'count': len(value),
                'attributes': value,
            }
        else:
            self.value = value

    def __bool__(self):
        return True


def build_response_from_invalid_request(invalid_request):
    message = '\n'.join(
        [
            '{}: {}'.format(err['parameter'], err['message'])
            for err in invalid_request.errors
        ]
    )

    return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, message)
