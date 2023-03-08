from fastapi import UploadFile
from os import remove
from os.path import abspath


def save_uploaded_file(file: UploadFile) -> str:
    """
    saves the file uploaded using rest api endpoint to temp folder to be used in processing the request
        Parameters:
            file (UploadFile): file uploaded using fast api UploadFile Object
        Returns:
            file_location (str): path to the saved file in temp folder
    """

    file_location = f"temp/{file.filename}"
    file_location = abspath(file_location)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return file_location


def remove_uploaded_file(file_location: str) -> None:
    """
    remove file from file location
        Parameters:
            file_location (str): location of file that need to be deleted
    """
    remove(file_location)
