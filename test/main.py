import sys
from fastapi import FastAPI, File, UploadFile
import uvicorn
from pydantic import BaseModel

sys.path.append("./")
from fastapi_frame_stream import FrameStreamer

app = FastAPI()
fs = FrameStreamer()


class InputImg(BaseModel):
    img_base64str : str

@app.get('/')
def home():
    return {'ok'}

@app.post("/send_frame_from_string/{img_id}")
async def send_frame_from_string(img_id: str, d:InputImg):
    await fs.send_frame(img_id, d.img_base64str)


@app.post("/send_frame_from_file/{img_id}")
async def send_frame_from_file(img_id: str, file: UploadFile = File(...)):
    await fs.send_frame(img_id, file)


@app.get("/video_feed/{img_id}")
async def video_feed(img_id: str):
    return fs.get_stream(img_id)


if __name__ == '__main__':
    # start the flask app
    uvicorn.run(app, host="0.0.0.0", port=6064)