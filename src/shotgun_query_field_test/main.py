import argparse
from typing import Dict

import shotgun_query_field_test.shotgun


def main(project_id: int):
    sequences = shotgun_query_field_test.shotgun.get_all_sequences_for_project_id(project_id)
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
    # TODO: Export to HTML.


def parse() -> Dict[str, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument('--project_id', type=int, help='The Project ID to get all sequences for.')
    args = parser.parse_args()
    return dict(args.__dict__)


if __name__ == "__main__":
    params = parse()
    main(**params)



