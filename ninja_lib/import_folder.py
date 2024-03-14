import importlib
import os
from pathlib import Path


def dynamic_import_from_folder(folder_path):
    folder_path = Path(folder_path)
    module_list = []

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".py"):
                module_path = Path(root) / file_name
                module_name = module_path.with_suffix("").as_posix().replace("/", ".")
                module = importlib.import_module(module_name)
                module_list.append(
                    {
                        "module": module,
                        "module_name": module_name,
                    }
                )

    return module_list
