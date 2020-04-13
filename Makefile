test:
	export APP_CONFIG=test;	pytest
dev:
	export APP_CONFIG=dev; python blog.py
db:
	sqlite3 data/db.sqlite3
migrate:
	export APP_CONFIG=dev; flask db migrate
upgrade:
	export APP_CONFIG=dev; flask db upgrade
freeze:
	pip freeze > requirements.txt