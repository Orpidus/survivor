from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage


def send_push_message(token, message, data=None):
    try:
        PushClient().publish(
            PushMessage(
                to=token,
                body=message,
                data=data
            )
        )
    except:
        pass
