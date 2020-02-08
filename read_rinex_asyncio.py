import asyncio
import os
import glob
import time
from typing import List

import aiofiles
import aiohttp

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

    async def process(self) -> None:
        await self._read()
        await self._http_post()
        print(self)

    async def _read(self) -> None:
        async with aiofiles.open(self.filename, 'r') as f:
            self.lines = await f.readlines()
        self.file_length = len(self.lines)

    async def _http_post(self) -> None:
        payload = {
            'filename': self.filename,
            'length': self.file_length
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(POST_URL, data=payload) as resp:
                self.http_response = resp.status


async def main(rinex_filenames: List[str]) -> None:
    rinex_files = [RinexFile(filename) for filename in rinex_filenames]
    tasks = []
    for rinex_file in rinex_files:
        tasks.append(rinex_file.process())
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    filenames = sorted(glob.glob(RINEX_DIR))
    print(f"Found {len(filenames)} RINEX files")

    t0 = time.perf_counter()
    asyncio.run(main(filenames))
    elapsed = time.perf_counter() - t0
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")