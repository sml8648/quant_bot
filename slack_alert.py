import urllib3
import json
import traceback

webhook_url = 'https://hooks.slack.com/services/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'

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