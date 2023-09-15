# -*- coding: utf-8 -*-


DOCUMENTATION = '''
---
module: azure_devops_pat
short_description: Manage Azure DevOps Personal Access Tokens (PATs)
description:
    - This module allows you to create, update, revoke, retrieve, and list Personal Access Tokens (PATs) in Azure DevOps.
version_added: "1.0"
author:
options:
    tenant_id:
        description:
            - Azure AD Tenant ID.
        required: true
    client_id:
        description:
            - Azure AD Application (Client) ID.
        required: true
    client_secret:
        description:
            - Azure AD Application Client Secret.
        required: true
    username:
        description:
            - Azure AD Username for authentication.
        required: true
    password:
        description:
            - Azure AD Password for authentication.
        required: true
    organization_name:
        description:
            - Name of the Azure DevOps organization.
        required: true
    token_name:
        description:
            - The display name for the PAT (Personal Access Token).
        required: false
        default: "MyToken"
    token_id:
        description:
            - The authorization ID of the PAT to update, revoke, or retrieve.
        required: false
    action:
        description:
            - The action to perform on the PAT (create, update, revoke, get, list).
        required: true
        choices:
            - create
            - update
            - revoke
            - get
            - list
'''


EXAMPLES = '''
    - name: Create a new PAT
      azure_auth:
        tenant_id: "{{ azure_tenant_id }}"
        client_id: "{{ azure_client_id }}"
        client_secret: "{{ azure_client_secret }}"
        username: "{{ azure_username }}"
        password: "{{ azure_password }}"
        organization_name: "{{ azure_organization_name }}"
        token_name: "MyNewToken"
        action: create
      register: create_pat_result

    - name: Display PAT Token
      debug:
        var: create_pat_result.pat_token

    - name: Update PAT
      azure_auth:
        tenant_id: "{{ azure_tenant_id }}"
        client_id: "{{ azure_client_id }}"
        client_secret: "{{ azure_client_secret }}"
        username: "{{ azure_username }}"
        password: "{{ azure_password }}"
        organization_name: "{{ azure_organization_name }}"
        token_name: "MyUpdatedToken"
        token_id: "{{ create_pat_result.message.authorizationId }}"
        action: update
      register: update_pat_result

    - name: Display Updated PAT Token
      debug:
        var: update_pat_result.message

    - name: Revoke PAT
      azure_auth:
        tenant_id: "{{ azure_tenant_id }}"
        client_id: "{{ azure_client_id }}"
        client_secret: "{{ azure_client_secret }}"
        username: "{{ azure_username }}"
        password: "{{ azure_password }}"
        organization_name: "{{ azure_organization_name }}"
        token_id: "{{ create_pat_result.message.authorizationId }}"
        action: revoke
      register: revoke_pat_result

    - name: Display Revoke Result
      debug:
        var: revoke_pat_result.message

    - name: Get PAT Info
      azure_auth:
        tenant_id: "{{ azure_tenant_id }}"
        client_id: "{{ azure_client_id }}"
        client_secret: "{{ azure_client_secret }}"
        username: "{{ azure_username }}"
        password: "{{ azure_password }}"
        organization_name: "{{ azure_organization_name }}"
        token_id: "{{ create_pat_result.message.authorizationId }}"
        action: get
      register: get_pat_result

    - name: Display PAT Info
      debug:
        var: get_pat_result.message

    - name: List All PATs
      azure_auth:
        tenant_id: "{{ azure_tenant_id }}"
        client_id: "{{ azure_client_id }}"
        client_secret: "{{ azure_client_secret }}"
        username: "{{ azure_username }}"
        password: "{{ azure_password }}"
        organization_name: "{{ azure_organization_name }}"
        action: list
      register: list_pats_result

    - name: Display List of PATs
      debug:
        var: list_pats_result.message
'''

RETURN = '''
message:
    description: The result message from the Azure DevOps PAT operation.
    type: str
    returned: always
pat_token:
    description: The Personal Access Token (PAT) token value.
    type: str
    returned: when PAT is created
'''


from ansible.module_utils.basic import AnsibleModule
import json
import requests

def azure_auth_module():
    module_args = dict(
        tenant_id=dict(type='str', required=True),
        client_id=dict(type='str', required=True),
        client_secret=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True),
        organization_name=dict(type='str', required=True),
        token_name=dict(type='str', required=False),
        action=dict(type='str', required=False, default='create', choices=['create', 'update', 'revoke', 'get', 'list']),
        token_id=dict(type='str', required=False),
    )

    result = dict(
        changed=False,
        message='',
        pat_token='',
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    # This is the Azure DevOps scope and is static
    scope = "499b84ac-1321-427f-aa17-267ca6975798/.default"

    # Define the Azure AD token endpoint
    token_url = (
        f"https://login.microsoftonline.com/{module.params['tenant_id']}/oauth2/v2.0/token"
    )

    # Define the token request payload
    token_data = {
        "grant_type": "password",
        "client_id": module.params['client_id'],
        "client_secret": module.params['client_secret'],
        "username": module.params['username'],
        "password": module.params['password'],
        "scope": scope,
    }

    try:
        # Send a POST request to acquire a token
        token_response = requests.post(token_url, data=token_data, timeout=10)

        # Check if the token acquisition was successful
        if token_response.status_code == 200:
            token_info = token_response.json()
            result['pat_token'] = token_info["access_token"]
            result['message'] = 'Authentication successful'
        else:
            result['message'] = 'Failed to create access Token'
            module.fail_json(msg=result['message'])

    except Exception as e:
        module.fail_json(msg=f"Error: {str(e)}")

    if module.params['action'] == 'create':
        if not module.params['token_name']:
            module.fail_json(msg="Token name is required for updating a PAT")

        api_url = f"https://vssps.dev.azure.com/{module.params['organization_name']}/_apis/tokens/pats?api-version=7.0-preview.1"

        # Define the token request payload
        api_data = json.dumps(
            {"displayName": f"{module.params['token_name']}", "scope": "vso.code"}
        )

        api_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {result['pat_token']}",
        }

        try:
            # Send POST response to create PAT
            response = requests.post(api_url, headers=api_headers, data=api_data, timeout=10)
            if response.status_code == 200:
                pat_info = response.json()
                result['pat_token'] = pat_info["patToken"]["token"]
            else:
                result['message'] = f"Access code {module.params['token_name']} failed to create"
                module.fail_json(msg=result['message'])
        except Exception as e:
            module.fail_json(msg=f"Error: {str(e)}")

    elif module.params['action'] == 'update':
        if not module.params['token_id']:
            module.fail_json(msg="Token ID is required for updating a PAT")

        api_url = f"https://vssps.dev.azure.com/{module.params['organization_name']}/_apis/tokens/pats?&api-version=7.0-preview.1"

        # Define the token request payload
        api_data = json.dumps(
            {"authorizationId": f"{module.params['token_id']}", "displayName": f"{module.params['token_name']}"}
        )

        api_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {result['pat_token']}",
        }

        try:
            # Send PUT response to update PAT
            response = requests.put(api_url, headers=api_headers, data=api_data, timeout=10)
            if response.status_code == 200:
                result['message'] = "PAT updated successfully"
            else:
                result['message'] = f"Failed to update PAT with ID {module.params['token_id']}"
                module.fail_json(msg=result['message'])
        except Exception as e:
            module.fail_json(msg=f"Error: {str(e)}")

    elif module.params['action'] == 'revoke':
        if not module.params['token_id']:
            module.fail_json(msg="Token ID is required for revoking a PAT")

        api_url = f"https://vssps.dev.azure.com/{module.params['organization_name']}/_apis/tokens/pats?authorizationId={module.params['token_id']}&api-version=7.0-preview.1"

        api_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {result['pat_token']}",
        }

        try:
            # Send DELETE response to revoke PAT
            response = requests.delete(api_url, headers=api_headers, timeout=10)
            if response.status_code == 204:
                result['message'] = "PAT revoked successfully"
            else:
                result['message'] = f"Failed to revoke PAT with ID {module.params['token_id']}"
                module.fail_json(msg=result['message'])
        except Exception as e:
            module.fail_json(msg=f"Error: {str(e)}")

    elif module.params['action'] == 'get':
        if not module.params['token_id']:
            module.fail_json(msg="Token ID is required for getting PAT info")

        api_url = f"https://vssps.dev.azure.com/{module.params['organization_name']}/_apis/tokens/pats?authorizationId={module.params['token_id']}&api-version=7.0-preview.1"

        api_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {result['pat_token']}",
        }

        try:
            # Send GET response to get PAT info
            response = requests.get(api_url, headers=api_headers, timeout=10)
            if response.status_code == 200:
                pat_info = response.json()
                result['message'] = pat_info
            else:
                result['message'] = f"Failed to get PAT info for ID {module.params['token_id']}"
                module.fail_json(msg=result['message'])
        except Exception as e:
            module.fail_json(msg=f"Error: {str(e)}")

    elif module.params['action'] == 'list':
        api_url = f"https://vssps.dev.azure.com/{module.params['organization_name']}/_apis/tokens/pats?api-version=7.0-preview.1"

        api_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {result['pat_token']}",
        }

        try:
            # Send GET response to list all PATs
            response = requests.get(api_url, headers=api_headers, timeout=10)
            if response.status_code == 200:
                pat_info = response.json()
                result['message'] = pat_info
            else:
                result['message'] = "Failed to list PATs"
                module.fail_json(msg=result['message'])
        except Exception as e:
            module.fail_json(msg=f"Error: {str(e)}")

    module.exit_json(**result)


if __name__ == '__main__':
    azure_auth_module()
