.PHONY: run
run:
	@python manage.py runserver $(port)

install:
	@pip install $(package)

csu:
	@python manage.py createsuperuser

mms:
	@python manage.py makemigrations

migrate:
	@python manage.py migrate

shell:
	@python manage.py shell

dbshell:
	@python manage.py dbshell

test:
	@pytest

clean:
	@Get-ChildItem -Path . -Recurse -Directory -Filter '__pycache__' | ForEach-Object { Remove-Item -Recurse -Force $_.FullName }



help:
	@echo "Usage: make [command]"
	@echo "Available commands"
	@echo "run	- run django server"
	@echo "install	- install python package"
	@echo "csu	-	createsuperuser"
	@echo "mms	-	makemigrations"
	@echo "migrate	- migrate migrations"
	@echo "shell	- Open shell"
	@echo "dbshell	- Open dbshell"
	@echo "test	- run test"
