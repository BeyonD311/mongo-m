import os
from pathlib import Path
from src.mongo_migrate.core import check_catalog, create_catalog

__all__ = ["create_migration_catalog"]


def create_migration_catalog():
    path = Path(f"{os.getcwd()}/migration")
    if not check_catalog(path.name):
        create_catalog(path.name)


