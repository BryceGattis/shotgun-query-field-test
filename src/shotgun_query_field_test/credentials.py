import keyring


def get_credential_from_keyring_or_error(service_name: str, username: str) -> str:
    password = keyring.get_password(service_name, username)
    if not password:
        raise EnvironmentError(f"Could not retrieve password for username: '{username}' "
                               f"for service: '{service_name}' from keyring.")
    return password
