.PHONY: install dev test
install:
python -m venv .venv && . .venv/bin/activate && pip install -U pip -r requirements.txt

dev:
. .venv/bin/activate && PORT=${PORT:-8080} uvicorn src.api.server:app --host 0.0.0.0 --port $$PORT

test:
. .venv/bin/activate && python -c "print('no tests yet')"
