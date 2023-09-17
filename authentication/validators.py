import re


def validate_data(data):
    email_regex = r'^\w+([.-]?\w+)*@(gmail|hotmail|outlook)\.com$'
    phone_regex = r'^(\\+34|0034|34)?[ -]*(6|7)[ -]*([0-9][ -]*){8}$'

    if not re.match(email_regex, data.get('email')):
        raise ValueError('email malformed')

    if len(data.get('name')) < 3:
        raise ValueError('name must have more than 3 characters')

    if len(data.get('last_name')) < 3:
        raise ValueError('lastName must have more than 3 characters')

    if not re.match(phone_regex, data.get('phone_number')):
        raise ValueError('phone malformed')
