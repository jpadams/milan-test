"""Create an environment with Python project and Poetry available"
"""

import dagger
from dagger import dag, function, object_type


@object_type
class Milan:
    
    @function
    async def test(self, source: dagger.Directory) -> dagger.Container:
        """Build a Container from a Python project"""
        return await (
            dag.container()
            .from_("ubuntu:latest")
            .with_exec(["apt", "update", "-y"])
            .with_exec(["apt", "update", "-y"])
            .with_exec(["apt", "install", "ca-certificates", "curl", "gnupg", "-y"])
            .with_exec(["apt", "install", "python3", "python-is-python3", "python3-venv", "-y"])
            .with_exec(["bash", "-c", "curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -"])
            .with_exec(["bash", "-c", "ln -T /opt/poetry/bin/poetry /usr/local/bin/poetry"])
            .with_directory("/src", source)
            .with_workdir("/src")
            .with_exec(["poetry", "install"])
			.sync()
        )
