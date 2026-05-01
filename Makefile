lint:
	uv run ruff check .
	uv run ruff format --check .

fixup:
	uv run ruff format .
	uv run ruff check --fix .

type-check:
	uv run ty check .

run:
	uv run uvicorrn run main:app

commit: lint type-check
	git add .
	git commit -m "$(msg)"