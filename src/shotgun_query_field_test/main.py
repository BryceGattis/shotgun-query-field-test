import functools
import getpass
import pprint
from typing import Any, Callable, Dict, List, Tuple, Union

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


def get_query_field_value(entity_type: str, field_name: str, entity_id: int) -> str:
    sg = get_shotgun_instance()
    schema = sg.schema_field_read(entity_type, field_name)
    # Excellent debugging tool for this kind of job.
    pprint.pprint(schema)
    if not schema:
        raise ValueError(f"Unable to find field: {field_name} on entity type: {entity_type}")
    properties = schema[field_name]['properties']
    filters = properties['query']['value']['filters']
    converted_filters = _convert_query_filters_to_queryable_list(filters, entity_id)
    query_entity_type = properties['query']['value']['entity_type']
    query_function_for_summary_type = _get_query_function_for_summary_type(properties['summary_default']['value'])
    query_field_value = query_function_for_summary_type(
        query_entity_type,
        converted_filters,
        properties['summary_field']['value'],
        properties['summary_default']['value']
    )
    return query_field_value


def _convert_query_filters_to_queryable_list(filters: Dict[str, Any], entity_id: int) -> List[Union[List[str], Dict[str, Any]]]:
    queryable_list = []
    logical_operator = filters.get('logical_operator')
    is_complex_filter = True if logical_operator else False
    if is_complex_filter:
        filter_operator = 'all' if 'and' in logical_operator else 'any'
        child_filters = filters['conditions']
        converted_filters = []
        for child_filter in child_filters:
            converted_filter = _convert_query_filters_to_queryable_list(child_filter, entity_id)
            converted_filters.append(converted_filter)
        queryable_filter = {
            "filter_operator": filter_operator,
            "filters": converted_filters
        }
        queryable_list.append(queryable_filter)
        return queryable_list
    # This is not a complex filter.
    is_filter_active = filters['active']
    if not is_filter_active:
        return []
    path = filters['path']
    relation = filters['relation']
    # If this has "Current" in it then we need to instead filter by the ID we passed in.
    values = filters['values']
    converted_values = _convert_current_entity_values_to_passed_id(values, entity_id)
    return [path, relation, converted_values]


def _convert_current_entity_values_to_passed_id(values: List[Dict[str, str]], entity_id: int) -> List[Dict[str, str]]:
    converted_list = []
    for value in values:
        is_dict = isinstance(value, dict)
        if not is_dict:
            converted_list.append(value)
            continue
        parent_entity_token = value.get('valid')
        is_pointing_to_current_entity = True if parent_entity_token == "parent_entity_token" else False
        if not is_pointing_to_current_entity:
            converted_list.append(value)
            continue
        entity_type = value['type']
        new_value = {'type': entity_type, 'id': entity_id}
        converted_list.append(new_value)
    return converted_list


def _get_query_function_for_summary_type(summary_type: str) -> Callable[[str, List, str, str], Any]:
    if summary_type == "average":
        return _get_average_for_field


def _get_average_for_field(entity_type: str, filters: List[Union[List[str], Dict[str, Any]]],
                           field: str, summary_type: str) -> int:
    sg = get_shotgun_instance()
    summary = sg.summarize(entity_type, filters, [{"field": field, "type": summary_type}])
    return int(summary['summaries'][field])