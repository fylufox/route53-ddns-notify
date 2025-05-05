
def lambda_handler(event, context):
    """
    AWS Lambda function handler.
    """
    
    record_sets = event["detail"]["requestParameters"]["changeBatch"]["changes"]
    
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
    
    # Your code here
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }