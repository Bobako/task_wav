import uuid

import pydub
from werkzeug.datastructures.file_storage import FileStorage

from app import config

def get_path(file_uuid: uuid.UUID):
    return config["SITE"]["upload_folder"] + "/" + str(file_uuid) + ".mp3"


def convert_and_save(file: FileStorage):
    file_uuid = uuid.uuid4()
    filepath = get_path(file_uuid)
    pydub.AudioSegment.from_file(file.stream).export(filepath, format="mp3")
    return file_uuid
    
    