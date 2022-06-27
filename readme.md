# fastapi-frame-stream

Package to easily stream individual frames (MJPEG) using FastAPI.

FastAPI server for publishing and viewing MJPEG streams.

## Quick start

### Installing

```cmd
pip install fastapi-frame-stream
```

#### Requirements

- [FastAPI](https://fastapi.tiangolo.com/)
- [uvicorn](https://www.uvicorn.org/)

<details>
  <summary><i>NOTE:</i></summary>
  This package will also automatically install:

- imutils
- opencv-python
- python-miltipart

</details>

### How to use

#### Server

You can create a simple FastAPI server where it is possible to publish and get multiple streams.

![usage code](./_readme_imgs/usage_code.svg)

<details>
<summary><i>full code</i></summary>

```python
from fastapi import FastAPI, File, UploadFile
import uvicorn
from pydantic import BaseModel
from fastapi_frame_stream import FrameStreamer

app = FastAPI()
fs = FrameStreamer()

class InputImg(BaseModel):
    img_base64str : str


@app.post("/send_frame_from_string/{stream_id}")
async def send_frame_from_string(stream_id: str, d:InputImg):
    await fs.send_frame(stream_id, d.img_base64str)


@app.post("/send_frame_from_file/{stream_id}")
async def send_frame_from_file(stream_id: str, file: UploadFile = File(...)):
    await fs.send_frame(stream_id, file)


@app.get("/video_feed/{stream_id}")
async def video_feed(stream_id: str):
    return fs.get_stream(stream_id)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)
```

</details>

#### Client

Any client can view a published image (MJPEG) stream using a simple ```<img>``` tag:

![usage code](./_readme_imgs/client_code.svg)

<details>
<summary><i>full code</i></summary>

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Testing fastapi-frame-stream</title>
</head>
<body>
    <img src="http://localhost:5000/video_feed/my_new_stream001">
</body>
</html>
```

</details>

#### All together

It is possible to upload an image file directly...

![Server and client](https://raw.githubusercontent.com/TiagoPrata/fastapi-frame-stream/master/_readme_imgs/usage001.gif)

... or to use any kind of application to convert the frames to base64 and send it to the web server:

![Server and client](https://raw.githubusercontent.com/TiagoPrata/fastapi-frame-stream/master/_readme_imgs/usage002.gif)
