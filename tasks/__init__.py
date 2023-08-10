from invoke import Collection

from tasks.docker import docker
from tasks.linting import pylint, mypy, lint, test, black

ns = Collection()
ns.add_task(pylint)
ns.add_task(mypy)
ns.add_task(lint)
ns.add_task(test)
ns.add_task(black)

ns.add_collection(docker, "docker")
