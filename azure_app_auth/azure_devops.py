"""Azure application authentication module.
Used to authenticate to azure Oauth applications"""
from typing import Union
import json
import requests


def auth(
    tenant_id: str,
    client_id: str,
    client_secret: str,
    username: str,
    password: str,  # noqa: E501  # pylint: disable=line-too-long
) -> Union:
    """Authentication function.
    Used to obtain OAuth token for authenticating against Azure DevOps API"""

    # This is the Azure DevOps scope and is static
    scope = "499b84ac-1321-427f-aa17-267ca6975798/.default"

    # Define the Azure AD token endpoint
    token_url = (
        f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"  # noqa: E501
    )

    # Define the token request payload
    token_data = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password,
        "scope": scope,
    }
    # Send a POST request to acquire a token
    token_response = requests.post(token_url, data=token_data, timeout=10)

    # Check if the token acquisition was successful
    if token_response.status_code == 200:
        token_info = token_response.json()
        return token_info["access_token"]

    print(
        f"""Failed to acquire a token.
          Status code: {token_response.status_code}"""
    )
    print(token_response.text)
    return None


def create_pat(
    access_token: str, organization_name: str, token_name: str
) -> str:  # noqa: E501
    """Function to create PATs"""

    api_url = f"https://vssps.dev.azure.com/{organization_name}/_apis/tokens/pats?api-version=7.0-preview.1"  # noqa: E501  # pylint: disable=line-too-long

    # Define the token request payload
    api_data = json.dumps(
        {"displayName": f"{token_name}", "scope": "app_token"}
    )  # noqa: E501 # pylint: disable=line-too-long

    api_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    # Send POST response to create PAT
    response = requests.request(
        "POST", api_url, headers=api_headers, data=api_data, timeout=10
    )  # noqa: E501
    if response.status_code == 200:
        pat_info = response.json()
        return pat_info["patToken"]["token"]

    print(response.text)
    return f"Access code {token_name} failed to create"


def test():
    """Test function"""
    return 0
