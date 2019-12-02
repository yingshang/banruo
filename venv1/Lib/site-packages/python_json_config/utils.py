from typing import Union, List


def normalize_path(path: Union[str, List[str]]) -> List[str]:
    if isinstance(path, str):
        path = path.split(".")
    return path
