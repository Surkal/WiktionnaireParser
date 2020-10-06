test:
	PYTHONPATH=. pytest

coverage:
	PYTHONPATH=. coverage run -m pytest
