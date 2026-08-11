lint:
	uv run ruff check src
	uv run ruff format --check src

fixup:
	uv run ruff format src
	uv run ruff check --fix src	

type-check:
	uv run ty check .

run:
	uv run uvicorn src.main:app --host 0.0.0.0 --port 9000 --reload

commit: lint type-check
	git add .
	git commit -m "$(msg)"