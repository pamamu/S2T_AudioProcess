import os.path
import re

import src.utils.config as config


def check_file(file_path) -> tuple:
    """
    Method that checks the availability of the file which indicates the path.

    :param file_path: Path of the file to be checked
    :type file_path: str

    :return: It will return the filename and the extension if there isn't any error
    :rtype: tuple
    :raise FileNotFoundError: The file doesn't exist o has a non-compatible extension.

    :Example:

    >>> check_file("/home/user/file.mp3") # Correct path and extension file
    None

    >>> check_file("/home/user/file.docx") # Incorrect path and extension file
    FileNotFoundError - Extension Error

    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError("File not found")
    filename, file_extension = os.path.splitext(file_path)
    filename = os.path.basename(filename)
    if not re.match(r"(^.[a-zA-Z0-9]+$)", file_extension) or \
            file_extension[1:] not in config.audio_extensions:
        raise FileNotFoundError("Extension Error")
    return filename, file_extension


def check_folder(folder_path, creation=False):
    """
    TODO

    :param folder_path:
    :param creation:
    :return:
    """
    if not os.path.isdir(folder_path):
        if creation:
            os.makedirs(folder_path)
        else:
            raise FileNotFoundError("Folder not found")


def folder_to_dict(path, max_depth) -> dict:
    """
    Method that given a parent folder and a number of iterations returns a dictionary with the folder structure

    :param path: Initial path
    :type path: str
    :param max_depth: Maximum number of iterations - depth of scanning. Less than 2 indicates that only the given
        folder is analyzed
    :type max_depth: int

    :return: Dictionary with file structure
    :rtype: dict
    :raise FileNotFoundError: The file or folder doesn't exist

    :Example:

    >>> folder_to_dict("/usr/local/share/man", 2) # Correct path
    {'name': 'man', 'type': 'folder', 'children':  [{'name': 'whatis', 'type': 'file'},
                                                    {'name': 'man1', 'type': 'folder'}]}

    >>> folder_to_dict("/usr/local/share/man", 1) # Correct path
    {'name': 'man', 'type': 'folder'}

    >>> folder_to_dict("/home/wrongfolder") # Incorrect path
    FileNotFoundError

    """
    if not os.path.exists(path):
        raise FileNotFoundError
    max_depth -= 1
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "folder"
        if max_depth > 0:
            d['children'] = [folder_to_dict(os.path.join(path, x), max_depth) for x in os.listdir(path)]
    else:
        d['type'] = "file"
    return d
