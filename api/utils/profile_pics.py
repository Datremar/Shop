import hashlib
import datetime
import os

import aiofiles
from fastapi import UploadFile


async def save_pic(img: UploadFile) -> str:
    hash = hashlib.sha256(str(datetime.datetime.now()).encode(encoding="utf-8")).hexdigest()

    img_path = f"resources/{hash}.jpg"

    async with aiofiles.open(img_path, 'wb') as out_file:
        while content := await img.read(1024):  # async read chunk
            await out_file.write(content)

    return img_path


async def update_pic(img_path: str, img: UploadFile):
    os.remove(img_path)

    async with aiofiles.open(img_path, 'wb') as out_file:
        while content := await img.read(1024):  # async read chunk
            await out_file.write(content)


async def delete_pic(img_path: str):
    os.remove(img_path)

