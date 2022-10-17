import requests

from prefect import Task


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
