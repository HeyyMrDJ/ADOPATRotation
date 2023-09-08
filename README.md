# Patty
Patty is an Azure DevOps PAT tool for managing PATs

# How to use
You will need the following:
- Azure AD Tenant ID
- Azure App Registration Client ID
- Azure App Registration Client Secret
- Azure AD Username
- Azure AD Password
- Azure DevOps Organization Name

In addition to the above you will need to provide a PAT Token name for creation and deletion, and the token_id for get, update, and revoke

### Create
```console
python3 patty.py create --tenant_id YourTenantID --client_id YourClientID --client_secret YourClientSecret --username YourUsername --password YourPassword --organization_name YourOrganization --token_name YourTokenName
```
### List
```console
python3 patty.py list --tenant_id YourTenantID --client_id YourClientID --client_secret YourClientSecret --username YourUsername --password YourPassword --organization_name YourOrganization
```
### Get
```console
python3 patty.py list --tenant_id YourTenantID --client_id YourClientID --client_secret YourClientSecret --username YourUsername --password YourPassword --organization_name YourOrganization --token_id YourTokenID
```
### Update
```console
python3 patty.py list --tenant_id YourTenantID --client_id YourClientID --client_secret YourClientSecret --username YourUsername --password YourPassword --organization_name YourOrganization --token_id YourTokenID
```
### Revoke
```console
python3 patty.py list --tenant_id YourTenantID --client_id YourClientID --client_secret YourClientSecret --username YourUsername --password YourPassword --organization_name YourOrganization --token_id YourTokenID
```
