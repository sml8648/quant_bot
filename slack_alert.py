import urllib3
import json
import traceback
import base64

f = open("webhook_url.txt", 'r')
webhook_url = f.readline().strip()
webhook_url = bytes(webhook_url, 'utf-8')
webhook_url = webhook_url.decode('ascii')
webhook_url = base64.b64decode(webhook_url)
webhook_url = webhook_url.decode('ascii')

# Send Slack notification based on the given message
def slack_notification(message):
    try:
        slack_message = {'text': message}

        http = urllib3.PoolManager()
        response = http.request('POST',
                                webhook_url,
                                body = json.dumps(slack_message),
                                headers = {'Content-Type': 'application/json'},
                                retries = False)
    except:
        traceback.print_exc()

    return True
