import requests
import boto3
from prefect import Task
import datetime


@Task
def submit_to_email_sanitizer(metadata: str, replacement_email: str = ""):
    """
    A simple script to clean out email addresses from a JSON-formatted string of metadata
    """
    sanitizer_url = "https://emailsanitizer.labs.dans.knaw.nl"
    response = requests.post(
        url=sanitizer_url,
        json={
            "replacement_email": replacement_email,
            "metadata": metadata
        }
    )
    if response.status_code == 200:
        return response
    else:
        raise Exception(f"Unexpected response code: {response.status_code}. Details: {response.__dict__}")


@Task
def log_to_cloudwatch(
        message: str,
        aws_region: str = 'eu-west-1'
):
    """
    Simple client to log specific log lines to AWS Cloudwatch.
    """
    client = boto3.client('logs', region_name=aws_region)
    log_event = client.put_log_events(
        logGroupName=LOG_GROUP_NAME,
        logStreamName=LOG_STREAM_NAME,
        logEvents=[
            {
                "timestamp": datetime.datetime.now(),
                "message": message
            }
        ]
    )
