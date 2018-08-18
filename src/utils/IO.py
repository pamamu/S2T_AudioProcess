import os.path
import re

import src.utils.config as config


def check_file(file_path):
    """
    Method that checks the availability of the file which indicates the path.
    :param file_path: Path of the file to be checked
    :return: None
    :raise FileNotFoundError: The file doesn't exist o has a non-compatible extension.
    """
    if not os.path.isfile(file_path): raise FileNotFoundError("File not found")
    filename, file_extension = os.path.splitext(file_path)
    if not re.match(r"(^.[a-zA-Z0-9]+$)", file_extension) or \
            file_extension[1:] not in config.audio_extensions:
        raise FileNotFoundError("Extension Error")


def folder_to_dict(path, max_depth):
    """
    Method that given a parent folder and a number of iterations returns a dictionary with the folder structure
    :param path: Initial path
    :param max_depth: Maximum number of iterations - depth of scanning.
    <2 indicates that only the given folder is analyzed
    :return: Dictionary with file structure
    :raise FileNotFoundError: The file or folder doesn't exist
    """
    if not os.path.exists(path):
        raise FileNotFoundError
    max_depth -= 1
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "folder"
        if (max_depth > 0):
            d['children'] = [folder_to_dict(os.path.join(path, x), max_depth) for x in os.listdir(path)]
    else:
        d['type'] = "file"
    return d
