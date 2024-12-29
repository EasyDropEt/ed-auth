# py
Template class for python backend servers.

## Features
- [x] RabbitMQ
- [x] Logging
- [X] Generic Helpers
- [ ] Kafka
- [ ] Redis
- [x] API: RequestHandler, FastAPI
- [x] Dockerfile
- [x] Makefile
- [x] CI/CD
- [x] Entry point file
- [x] Configfile / Configuration
- [x] Websockets

## Usage
The project's dependencies are managed by `poetry`. You can install the dependencies with:
```bash
poetry install
```

`package.py` is the entry point file.

### Running the package
You can run the package inside of a virtual environment:
```bash
poetry shell
make run
```

or with `docker`:
```bash
make run_docker
```


### Running the tests
You can run the tests inside of a virtual environment:
```bash
poetry shell
make test
```
or with `docker`:
```bash
make test_docker
```
