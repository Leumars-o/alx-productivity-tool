import os
from dotenv import load_dotenv

load_dotenv()

def load_credentials():
    """ This function is responsible for extracting user data to be used for the intranet
    """
    credentials = []

    for key, value in os.environ.items():
        if key.startswith('ALX_USER_'):
            user_id = value.split('_')
            if user_id:
                credentials.append({'email': user_id[0], 'password': user_id[1], 'chat_id': int(user_id[2])})
    return credentials
