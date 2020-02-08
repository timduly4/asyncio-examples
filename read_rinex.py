import os
import glob
import time
from typing import List
import requests

RINEX_DIR = os.path.expanduser('~/Desktop/rinex_files/*.*o')
POST_URL = 'https://postman-echo.com/post'


class RinexFile:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.lines = []
        self.file_length = None
        self.http_response = None

    def __repr__(self) -> str:
        return (
            f"RINEX file, {os.path.basename(self.filename)}, "
            f"{self.file_length:6d} lines, HTTP POST response: {self.http_response}"
        )

    def process(self) -> None:
        with open(self.filename, 'r') as f:
            self.lines = f.readlines()
        self.file_length = len(self.lines)

        payload = {
            'filename': self.filename,
            'length': self.file_length
        }
        resp = requests.post(POST_URL, data=payload)
        self.http_response = resp.status_code

        print(self)


def main(rinex_filenames: List[str]) -> None:
    rinex_files = [RinexFile(filename) for filename in rinex_filenames]
    for rinex_file in rinex_files:
        rinex_file.process()


if __name__ == "__main__":
    filenames = sorted(glob.glob(RINEX_DIR))
    print(f"Found {len(filenames)} RINEX files")

    t0 = time.perf_counter()
    main(filenames)
    elapsed = time.perf_counter() - t0
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
