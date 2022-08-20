${VERSION}:
	@echo "__version__ = \"$(shell git describe --tag --always | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo "0.0.0")\"" > ${VERSION}
keys/:
	mkdir keys

keys/private.pem:keys/
	openssl genrsa -out keys/private.pem 2048

keys/public.pem:keys/private.pem
	openssl rsa -in keys/private.pem -outform PEM -pubout -out keys/public.pem
