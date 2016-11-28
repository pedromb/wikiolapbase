.PHONY: deps
deps:
	pip3 install -r requirements.txt

.PHONY: run
run:
	@python3 manage.py runserver