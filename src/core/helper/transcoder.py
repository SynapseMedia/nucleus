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
    return file_extension


def match_format(file, _format):
    extracted_format = extract_extension(file)
    is_default_format = extracted_format != _format

    return


