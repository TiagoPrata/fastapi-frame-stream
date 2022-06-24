#!/usr/bin/env python
"""Defines the FrameStreamer class and it's interface with the in memory SQLite datebase
"""

from typing import Any, Mapping, Union
import cv2
import imutils
import time
import base64
import numpy as np
import sqlite3
from fastapi import BackgroundTasks, File, UploadFile
from starlette.datastructures import UploadFile as starletteUploadFile
from fastapi.responses import StreamingResponse

__author__ = "Tiago Prata"
__credits__ = ["Tiago Prata"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Tiago Prata"
__email__ = "prataaa@hotmail.com"
__status__ = "Beta version"


SQLLITE_CONN_STR = "file:framestreamerdb1?mode=memory&cache=shared"

class FrameStreamer:
    """The FrameStreamer class allows you to send frames and visualize them as a stream
    """

    def __init__(self):
        self.conn = sqlite3.connect(SQLLITE_CONN_STR, uri=True)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS images (
                                                        id text PRIMARY KEY,
                                                        image text
                                                        )''')
        self.conn.commit()



    def _get_image(self, img_id: str) -> Union[str, None]:
        """Get an image from the SQLite DB.

        Args:
            img_id (str): ID (primary key) of the image to be retrieved in the DB

        Returns:
            Union[str, None]: Image (in base64)
        """

        img = None
        self.conn = sqlite3.connect(SQLLITE_CONN_STR, uri=True)
        c = self.conn.cursor()
        c.execute("SELECT image FROM images WHERE id = (?)", (img_id, ))
        rows = c.fetchall()

        try:
            img = rows[0][0]
        except:
            pass

        return img



    async def _store_image_str(self, img_id: str, img_str_b64: str) -> None:
        """Store an image string (in base64) to the DB.

        Args:
            img_id (str): ID (primary key) of the image.
            img_str_b64 (str): Image string (in base64)
        """

        try:
            self.conn = sqlite3.connect(SQLLITE_CONN_STR, uri=True)
            c = self.conn.cursor()
            c.execute("INSERT OR IGNORE INTO images VALUES (?,?)", (img_id, img_str_b64, ))
            c.execute("UPDATE images SET image = (?) WHERE id = (?)", (img_str_b64, img_id, ))
            self.conn.commit()
        except:
            pass


    
    async def _image_file_to_base64(self, file: UploadFile = File(...)) -> str:
        """Convert a loaded image to Base64 
        
        Args:
            file (UploadFile, optional): Image file to be converted.
        
        Returns:
            str: Image converted (in Base64)
        """
        image_file = await file.read()
        return base64.b64encode(image_file).decode("utf-8")



    async def send_frame(self, stream_id: str, frame: Union[str, UploadFile, bytes]) -> None:
        """Send a frame to be streamed.

        Args:
            stream_id (str): ID (primary key) of the frame
            frame (Union[str, UploadFile, bytes]): Frame (image) to be streamed.
        """

        if isinstance(frame, str):
            await self._store_image_str(stream_id, frame)
        elif isinstance(frame, starletteUploadFile):
            img_str = await self._image_file_to_base64(frame)
            await self._store_image_str(stream_id, img_str)
        elif isinstance(frame, bytes):
            img_str = base64.b64encode(frame).decode("utf-8")
            await self._store_image_str(stream_id, img_str)



    def _readb64(self, encoded_img: str) -> Any:
        """Decode an image (in base64) to an OpenCV image

        Args:
            encoded_img (str): Image (in base64)

        Returns:
            Any: Image decoded from OpenCV
        """

        if encoded_img == None: return None

        nparr = np.frombuffer(base64.b64decode(encoded_img), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img



    def _start_stream(self, img_id: str, freq: int = 30):
        """Continuous loop to stream the frame from SQLite to html image/jpeg format

        Args:
            img_id (str): ID (primary key) of the image in the DB
            freq (int, optional): Loop frequency. Defaults to 30.

        Yields:
            bytes: HTML containing the bytes to plot the stream
        """

        sleep_duration = 1.0 / freq

        while True:
            time.sleep(sleep_duration)
            try:
                frame = self._readb64(self._get_image(img_id))
            except:
                pass
            if frame is None: continue

            frame = imutils.resize(frame, width=680)
            output_frame = frame.copy()

            if output_frame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", output_frame)
            if not flag:
                continue
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')



    def get_stream(self, stream_id: str, freq: int = 30, status_code: int = 206,
                    headers: Union[Mapping[str, str], None] = None,
                    background: Union[BackgroundTasks, None] = None) -> StreamingResponse:
        """Get an stream of frames

        Args:
            stream_id (str): ID (primary key) of the stream to be retrieved
            freq (int, optional): Frequency of the continuous loop retrieval (in Hz). Defaults to 30.
            status_code (int, optional): HTTP response status code. Defaults to 206.
            headers (Union[Mapping[str, str], None], optional): HTTP headers. Defaults to None.
            background (Union[BackgroundTasks, None], optional): FastAPI background. Defaults to None.

        Returns:
            StreamingResponse: FastAPI StreamingResponse
        """
        
        return StreamingResponse(self._start_stream(stream_id, freq),
                                media_type="multipart/x-mixed-replace;boundary=frame",
                                status_code=status_code,
                                headers=headers,
                                background=background)