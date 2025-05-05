import os
import slack_webhook

def lambda_handler(event, context):
    """
    AWS Lambda function handler.
    """
    print("Get event data:\n"+str(event))
    
    SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
    
    record_sets = event["detail"]["requestParameters"]["changeBatch"]["changes"]
    print("Get record sets:\n"+str(record_sets))
    
    if len(record_sets) == 2:
        domain_name = []
        is_create = False
        is_delete = False
        address = ""
        for record_set in record_sets:
            if record_set["action"] == "CREATE":
                is_create = True
                address = record_set["resourceRecordSet"]["resourceRecords"][0]["value"]
            elif record_set["action"] == "DELETE":
                is_delete = True
            domain_name.append(record_set["resourceRecordSet"]["name"].rstrip('.'))
        if is_create and is_delete and domain_name[0] == domain_name[1]:
            del record_sets[1]
            record_sets[0]["action"] = "UPSERT"
            record_sets[0]["resourceRecordSet"]["name"] = domain_name[0]
            record_sets[0]["resourceRecordSet"]["resourceRecords"][0]["value"] = address
    
    attachments = []
    payload = dict()
    responses = []
    for record_set in record_sets:
        attachments.append(slack_webhook.make_payload_attachments(
            record_set["action"],
            record_set["resourceRecordSet"]["name"],
            record_set["resourceRecordSet"]["resourceRecords"][0]["value"]
        )
        )
        payload["attachments"] = attachments
        print("Send payload:\n"+str(payload))
        
        responses.append(slack_webhook.push_slack_webhook(
            payload,
            SLACK_WEBHOOK_URL
            )
        )
    
    request_false = False
    for response in responses:
        if response.status_code != 200:
            print(f"Error sending message to Slack: {response.status_code} - {response.text}")
            request_false = True
        else:
            print(f"Message sent to Slack successfully: {response.status_code} - {response.text}")
    
    if request_false:
        return {
            'statusCode': 500,
            'body': 'Error sending message to Slack'
        }
    else:
        return {
            'statusCode': 200,
            'body': 'Message sent to Slack successfully'
        }
