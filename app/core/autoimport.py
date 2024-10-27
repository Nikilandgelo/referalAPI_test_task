from importlib import import_module
from pkgutil import iter_modules


def make_autoimport(path_to_package: list[str], name_of_package: str) -> list:
    """
    Automatically import all submodules from a specified package.

    This function iterates through all modules in the given package path,
    imports each module, and returns a list of their names.

    Args:
        path_to_package (list[str]): A list of strings representing the path\
            to the package.
        name_of_package (str): The name of the package to import from.

    Returns:
        list: A list of strings containing the names of all imported\
            submodules.
    """
    all_submodules: list = []
    for module_info in iter_modules(path_to_package):
        _ = import_module(f".{module_info.name}", package=name_of_package)
        all_submodules.append(module_info.name)
    return all_submodules
