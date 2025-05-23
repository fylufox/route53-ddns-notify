import requests


def make_payload_attachments(action, record_name, address):
    if action == 'DELETE':
        color = '#dc143c'
    else:
        color = '#249B12'

    payload = {
        "color": f"{color}",
        "blocks": [dict(
            type="section",
            text=dict(
                type="mrkdwn",
                text=f"Action : {action}\nRecord Name : {record_name}\nIP Address : {address}"
            )
        )]
    }
    return payload


def push_slack_webhook(message, url):
    headers = {
        'Content-type': 'application/json'
    }
    data = '{}'.format(message)
    data = data.encode('utf-8')
    response = requests.post(
        url, headers=headers, data=data)
    return response
