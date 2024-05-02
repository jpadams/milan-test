"""Create an environment with Python project and Poetry available"
"""

import dagger
from dagger import dag, function, object_type


@object_type
class Milan:
    
    @function
    def poetry_base(self) -> dagger.Container:
        """Build an Ubuntu Container with Poetry"""
        return (
            dag.container()
            .from_("ubuntu:latest")
            .with_exec(["apt", "update", "-y"])
            .with_exec(["apt", "update", "-y"])
            .with_exec(["apt", "install", "ca-certificates", "curl", "gnupg", "-y"])
            .with_exec(["apt", "install", "python3", "python-is-python3", "python3-venv", "-y"])
            .with_exec(["bash", "-c", "curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -"])
            .with_exec(["bash", "-c", "ln -T /opt/poetry/bin/poetry /usr/local/bin/poetry"])
        )

    @function
    def test(self, source: dagger.Directory) -> dagger.Container:
        """Build an Ubuntu Container with Poetry"""
        return (
            self.poetry_base()
            .with_directory("/src", source)
            .with_workdir("/src")
            .with_exec(["poetry", "install"])
        )

    @function
    async def scan(self) -> str:
        """Scan with Trivy"""
        repo = "https://github.com/fpgmaas/cookiecutter-poetry-example"
        dir = dag.git(repo).branch("main").tree()
        return await dag.trivy().scan_container(self.test(dir))
