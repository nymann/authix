ensure-test-dependencies:
	command -v pytest 2>/dev/null || make install-tests

test: ${VERSION} ensure-test-dependencies keys/public.pem
	pytest tests/unit_tests


integration: ${VERSION} ensure-test-dependencies keys/public.pem
	pytest tests/integration_tests
