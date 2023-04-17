from deta import Deta


def download_file(drive: str, file_name: str) -> bytes:
    deta = Deta()
    drive = deta.Drive(drive)

    file = drive.get(file_name)

    return file.read()


def upload_file(drive: str, file_name: str, file: bytes):
    deta = Deta()
    drive = deta.Drive(drive)

    drive.put(file_name, file)
