from os.path import expanduser


class Credential:
    """Stores the user's name and password"""

    def __init__(self, username=None, password=None, api_id=None, key=None):
        self.username = username
        self.password = password

    @staticmethod
    def read_credential_from_file(cred_file=expanduser('~') + '/.veracoderc'):
        with open(cred_file) as credentialFile:
            username = credentialFile.readline().strip()
            password = credentialFile.readline().strip()
        return Credential(username, password)
