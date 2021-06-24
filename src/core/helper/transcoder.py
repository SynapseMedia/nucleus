import os
import mimetypes

mimetypes.init()


def extract_extension(file):
    """
    Extract file extension
    :param file:
    :return: string extension
    """
    _, file_extension = os.path.splitext(file)
    file_extension = file_extension.replace('.', '')
    return file_extension

