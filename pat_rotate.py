"""Python script to rotate ADO PATs using custom libraries"""
import argparse
from azure_app_auth import azure_devops


def parse_arguments():
    """Function to parse CLI arguments"""

    parser = argparse.ArgumentParser(
        description="Azure DevOps Authentication and Token Management"
    )  # noqa: E501  # pylint: disable=line-too-long
    parser.add_argument(
        "operation",
        choices=["create", "get", "revoke", "list", "update"],
        help="Operation to perform",
    )  # noqa: E501  # pylint: disable=line-too-long
    parser.add_argument(
        "--tenant_id", required=True, help="Azure AD Tenant ID"
    )  # noqa: E501  # pylint: disable=line-too-long
    parser.add_argument(
        "--client_id", required=True, help="Azure AD Client ID"
    )  # noqa: E501  # pylint: disable=line-too-long
    parser.add_argument(
        "--client_secret", required=True, help="Azure AD Client Secret"
    )  # noqa: E501  # pylint: disable=line-too-long
    parser.add_argument(
        "--username", required=True, help="Azure DevOps Username"
    )  # noqa: E501  # pylint: disable=line-too-long
    parser.add_argument(
        "--password", required=True, help="Azure DevOps Password"
    )  # noqa: E501  # pylint: disable=line-too-long
    parser.add_argument(
        "--organization_name",
        required=True,
        help="Azure DevOps Organization Name",  # noqa: E501  # pylint: disable=line-too-long
    )
    parser.add_argument("--token_name", help="Token Name for PAT operations")
    parser.add_argument("--token_id", help="Token ID for PAT operations")
    args = parser.parse_args()

    if args.operation in ["create", "update"] and args.token_name is None:
        parser.error(
            f"--token_name is required for the {args.operation} operation"
        )  # noqa: E501  # pylint: disable=line-too-long

    if args.operation in ["revoke", "get", "update"] and args.token_id is None:
        parser.error(
            f"--token_id is required for the {args.operation} operation"
        )  # noqa: E501  # pylint: disable=line-too-long

    return parser.parse_args()


def main():
    """Main Function"""
    args = parse_arguments()

    access_token = azure_devops.auth(
        args.tenant_id,
        args.client_id,
        args.client_secret,
        args.username,
        args.password,  # noqa: E501  # pylint: disable=line-too-long
    )

    if args.operation == "create":
        result = azure_devops.create_pat(
            access_token, args.organization_name, args.token_name
        )  # noqa: E501  # pylint: disable=line-too-long

    elif args.operation == "get":
        result = azure_devops.get_pat(
            access_token, args.organization_name, args.token_id
        )  # noqa: E501  # pylint: disable=line-too-long

    elif args.operation == "revoke":
        result = azure_devops.revoke_pat(
            access_token, args.organization_name, args.token_id
        )  # noqa: E501  # pylint: disable=line-too-long

    elif args.operation == "list":
        result = azure_devops.list_pats(access_token, args.organization_name)

    elif args.operation == "update":
        result = azure_devops.update_pat(
            access_token, args.organization_name, args.token_id, args.token_name
        )  # noqa: E501  # pylint: disable=line-too-long

    print(result)


if __name__ == "__main__":
    main()
