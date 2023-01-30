build:
	docker build -t test .

start:
	docker run --name test --rm -v C:/Users/kirill/PycharmProjects/lern_projects/docker/debug/debug.log:/app/debug/debug.log test

stop:
	docker stop test
	docker image rm test

rm:
	docker image rm test