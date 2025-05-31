test:
	pytest

run:
	python -m shotgun_query_field_test.main --project_id 85

install:
	python -m pip install .

install_for_test:
	 python -m pip install .[test]