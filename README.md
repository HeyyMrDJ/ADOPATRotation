# ADOPATRotation
Azure DevOps non-interactive PAT rotation

# How to use
You will need the following:
- Azure AD Tenant ID
- Azure App Registration Client ID
- Azure App Registration Client Secret
- Azure AD Username
- Azure AD Password
- Azure DevOps Organization Name

In addition to the above you will need to provide a PAT Token name to name the PAT

```console
python3 pat_rotate.py "TENTANT_ID" "CLIENT_ID" "CLIENT_SECRET" "USERNAME" "PASSWORD" "ORGANIZATION_NAME" "TOKEN_NAME"
```
