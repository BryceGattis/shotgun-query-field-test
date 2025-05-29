import functools
import os

import shotgun_api3

@functools.lru_cache()
def get_shotgun_instance() -> shotgun_api3.Shotgun:
    site_url = os.getenv("SHOTGUN_SITE_URL")
    if not site_url:
        raise EnvironmentError("SHOTGUN_SITE_URL not set, cannot get SG instance.")
    script_name = os.getenv("SHOTGUN_SCRIPT_NAME")
    if not script_name:
        raise EnvironmentError("SHOTGUN_SCRIPT_NAME not set, cannot get SG instance.")
    api_key = os.getenv("SHOTGUN_API_KEY")
    if not api_key:
        raise EnvironmentError("SHOTGUN_API_KEY not set, cannot get SG instance.")
    sg = shotgun_api3.Shotgun(site_url, script_name=script_name, api_key=api_key)
    return sg

def get_query_field_value(entity_type: str, field_name: str) -> str:
    sg = get_shotgun_instance()
    schema = sg.schema_field_read(entity_type, field_name)
    if not schema:
        raise ValueError(f"Unable to find field: {field_name} on entity type: {entity_type}")
