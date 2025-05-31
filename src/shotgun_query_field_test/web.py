from typing import Dict, List

import tabulate


def generate_table_for_entities_and_fields(entities: List[Dict[str, str]]):
    if not entities:
        return
    html = tabulate.tabulate(entities, headers="keys", tablefmt='html')
    # This will export to the current shell directory.
    with open('table.html', 'w') as f:
        f.write(html)
