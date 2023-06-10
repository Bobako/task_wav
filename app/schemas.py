create_user_request = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'}
    },
    'required': ['username']
}

create_audio_request = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'integer'},
        'token': {'type': 'string', 'format': 'uuid'},
    },
    'required': ['user_id', 'token']
}

get_record_request = {
    'type': 'object',
    'properties': {
        'user': {'type': 'integer'},
        'id': {'type': 'string', 'format': 'uuid'},
    },
    'required': ['user', 'id']
}