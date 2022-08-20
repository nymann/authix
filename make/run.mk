run: keys/public.pem
	uvicorn ${COMPONENT}.asgi:api --reload --port 8660 --host 0.0.0.0

.PHONY: run
