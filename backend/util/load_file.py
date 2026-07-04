import yaml
from pathlib import Path

def LoadYaml(path: Path):
    with open(path, "r") as f:
        return yaml.safe_load(f)