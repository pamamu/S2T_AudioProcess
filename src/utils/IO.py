import os.path
import re
import json
import shutil


def get_io_config() -> dict:
    """
    TODO DOCUMENTATION
    :return:
    """
    io_config_file = "src/configs/IO_config.json"
    io_config = json.loads(open(io_config_file).read())
    return io_config


def get_tmp_folder():
    """
    TODO DOCUMENTATION
    :return:
    """
    io_config = get_io_config()
    if not os.path.isdir(io_config['tmp_folder']):
        os.mkdir(io_config['tmp_folder'])
    return io_config['tmp_folder']


def get_tmp_splitted_folder():
    folder = os.path.join(get_tmp_folder(), 'audio_segments')
    if not os.path.isdir(folder):
        os.mkdir(folder)
    return folder


def check_audio_file(file_path) -> tuple:
    """
    Method that checks the availability of the file which indicates the path.

    :param file_path: Path of the file to be checked
    :type file_path: str

    :return: It will return the filename and the extension if there isn't any error
    :rtype: tuple
    :raise FileNotFoundError: The file doesn't exist o has a non-compatible extension.

    :Example:

    >>> check_audio_file("/home/user/file.mp3") # Correct path and extension file
    None

    >>> check_audio_file("/home/user/file.docx") # Incorrect path and extension file
    FileNotFoundError - Extension Error

    """

    io_config = get_io_config()

    if not os.path.isfile(file_path):
        raise FileNotFoundError("File not found")
    filename, file_extension = os.path.splitext(file_path)
    filename = os.path.basename(filename)
    if not re.match(r"(^.[a-zA-Z0-9]+$)", file_extension) or \
            file_extension[1:] not in io_config['allowed_extensions']:
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


def move_files(files, folder, audio_name):
    """
    TODO DOCUMENTATION
    :param files:
    :param folder:
    :param audio_name:
    :return:
    """
    check_folder(folder, True)
    clean_folder(os.path.join(folder, audio_name))
    check_folder(os.path.join(folder, audio_name), True)
    destination_paths = []
    for file in files:
        basename = os.path.basename(file)
        destination_path = os.path.join(folder, audio_name, basename)
        destination_paths.append(destination_path)
        shutil.move(file, destination_path)
    return destination_paths


def save_json(info, folder, audio_name):
    """
    TODO DOCUMENTATION
    :param info:
    :param folder:
    :param audio_name:
    :return:
    """
    check_folder(os.path.join(folder, audio_name), True)
    out_file = os.path.join(folder, audio_name, 'info.json')
    with open(out_file, 'w') as fp:
        json.dump(info, fp, indent=2)
    return out_file


def clean_folder(folder) -> None:
    """
    TODO DOCUMENTATION
    :param folder:
    :return:
    """
    if os.path.isdir(folder):
        shutil.rmtree(folder)


def clean_tmp_folder() -> None:
    """
    TODO DOCUMENTATION
    :return:
    """
    shutil.rmtree(get_tmp_folder())
