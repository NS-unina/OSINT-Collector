all: launcher

launcher:
	docker build --no-cache -t osint-collector-launcher -f launcher.Dockerfile ..

launcher-test:
	docker build --no-cache -t osint-collector-launcher-test -f test_launcher.Dockerfile ..