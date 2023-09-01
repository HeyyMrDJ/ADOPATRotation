"Test module"
from azure_app_auth import azure_devops


def test_add_numbers():
    "Test function"
    value = azure_devops.test()
    assert value == 0
