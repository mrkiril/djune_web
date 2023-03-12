MAIN_SERVICE = web_service

ps:
	docker compose ps

up:
	docker compose up -d
	docker compose ps

down:
	docker compose down

run:
	docker compose build --parallel --no-cache
	docker compose up -d
	docker compose ps

rebuild:
	docker compose build --parallel
	docker compose up -d
	docker compose ps

restart:
	docker compose restart $(MAIN_SERVICE)
	docker compose ps

bash:
	docker compose exec $(MAIN_SERVICE) bash