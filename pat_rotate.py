"""Python script to rotate ADO PATs using custom libraries"""
import sys
from azure_app_auth import azure_devops


if len(sys.argv[:]) < 8:
    print("Missing required arguments")
    sys.exit()
else:
    TENANT_ID = sys.argv[1]
    CLIENT_ID = sys.argv[2]
    CLIENT_SECRET = sys.argv[3]
    USERNAME = sys.argv[4]
    PASSWORD = sys.argv[5]
    ORGANZATION_NAME = sys.argv[6]
    TOKEN_NAME = sys.argv[7]

access_token = azure_devops.auth(
    TENANT_ID, CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD
)

result = azure_devops.create_pat(access_token, ORGANZATION_NAME, TOKEN_NAME)

print(result)
