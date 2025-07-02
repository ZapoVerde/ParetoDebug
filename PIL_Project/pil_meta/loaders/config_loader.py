# pil_meta/loaders/config_loader.py
"""
Config Loader (loaders)

Loads and validates the pilconfig.json configuration file for the PIL project.
All relevant paths are resolved as absolute, relative to the config file location.
"""

import json
from pathlib import Path

def load_config(config_path: str) -> dict:
    """
    Load the PIL project configuration from pilconfig.json and resolve all important paths.

    Args:
        config_path (str): Path to pilconfig.json file (absolute or relative)

    Returns:
        dict: Configuration fields as a dictionary, all relevant paths absolute.
    """
    config_file = Path(config_path).resolve()
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    # Validate required fields
    required = ["project_root", "output_dir"]
    missing = [k for k in required if k not in config]
    if missing:
        raise ValueError(f"Missing required config fields: {missing}")
    # Resolve all relevant paths to absolute (relative to config file's directory)
    base_dir = config_file.parent
    for field in [
        "project_root", "journal_path", "output_dir", "docs_dir", "vault_dir", "snapshot_dir"
    ]:
        if field in config:
            value = config[field]
            if not Path(value).is_absolute():
                config[field] = str((base_dir / value).resolve())
    # Always record the absolute config file path itself
    config["config_self_path"] = str(config_file)
    return config
