import functools
import getpass

import shotgun_api3

from shotgun_query_field_test.credentials import get_credential_from_keyring_or_error


@functools.lru_cache()
def get_shotgun_instance() -> shotgun_api3.Shotgun:
    username = getpass.getuser()
    site_url = get_credential_from_keyring_or_error('shotgun.api.url', username)
    script_name = get_credential_from_keyring_or_error('shotgun.api.script_name', username)
    api_key = get_credential_from_keyring_or_error('shotgun.api.api_key', username)
    sg = shotgun_api3.Shotgun(site_url, script_name=script_name, api_key=api_key)
    return sg


def get_query_field_value(entity_type: str, field_name: str) -> str:
    sg = get_shotgun_instance()
    schema = sg.schema_field_read(entity_type, field_name)
    if not schema:
        raise ValueError(f"Unable to find field: {field_name} on entity type: {entity_type}")
