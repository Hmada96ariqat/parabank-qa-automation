import yaml
import pytest


@pytest.fixture(scope="session")
def settings():
    with open("config/settings.yaml") as f:
        # converts yaml file to python dictionary
        return yaml.safe_load(f)
