def format_pydantic_error(error):
    body = error.errors()[0]
    return {
        'error': {
            'type': 'ValidationError',
            'message': f'{body["loc"][0]}: {body["msg"]}',
        }
    }
