# config/config_manager.py

import json
import os

CONFIG_PATH = os.environ.get("CONFIG_PATH", "config/config.json")

def load_config() -> dict:
    """Load configuration from JSON file."""
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(config: dict):
    """Save configuration to JSON file."""
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
