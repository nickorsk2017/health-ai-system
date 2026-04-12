.PHONY: install build inspect inspect-docker kill-inspector

run-dev:
	uv run visit_doctor_agent

build:
	docker build -t visit_doctor_agent .

inspect:
	make kill-inspector
	CLIENT_PORT=6302 SERVER_PORT=6303 npx @modelcontextprotocol/inspector uv run visit_doctor_agent

inspect-docker:
	make kill-inspector
	npx @modelcontextprotocol/inspector docker run -i --rm --env-file .env visit_doctor_agent

kill-inspector:
	kill -9 $$(lsof -t -i :6302 -i :6303) 2>/dev/null || true
