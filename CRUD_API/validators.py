def validate_data(data):

    if len(data.get('title')) < 3:
        raise ValueError('title must have more than 3 characters')

    if len(data.get('content')) < 3:
        raise ValueError('content must have more than 3 characters')
