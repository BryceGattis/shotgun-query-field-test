import argparse
from typing import Dict

import shotgun_query_field_test.shotgun
import shotgun_query_field_test.web


def main(project_id: int):
    """Find all sequences for the given project_id, then export sg_cut_duration and sg_ip_versions to an HTML table."""
    sequences = shotgun_query_field_test.shotgun.get_all_sequences_for_project_id(project_id)
    entities_to_export = []
    for sequence in sequences:
        sg_cut_duration = shotgun_query_field_test.shotgun.get_query_field_value(
            'Sequence',
            'sg_cut_duration',
            sequence['id']
        )
        sg_ip_versions = shotgun_query_field_test.shotgun.get_query_field_value(
            'Sequence',
            'sg_ip_versions',
            sequence['id']
        )
        entity = {
            'type': 'Sequence',
            'id': sequence['id'],
            'sg_cut_duration': sg_cut_duration,
            'sg_ip_versions': sg_ip_versions
        }
        entities_to_export.append(entity)
    shotgun_query_field_test.web.generate_table_for_entities_and_fields(entities_to_export)


def parse() -> Dict[str, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument('--project_id', type=int, help='The Project ID to export query field data for.')
    args = parser.parse_args()
    return dict(args.__dict__)


if __name__ == "__main__":
    params = parse()
    main(**params)



