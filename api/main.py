from fastapi import FastAPI, UploadFile
import uvicorn
from PIL import Image
from io import BytesIO
import base64

from model import create_model
from utils import predict_img, overlay_img, get_title

model = create_model()
model.load_weights("./weights/weights_03-12-22-510637.hdf5")

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Hello World"}

@app.post("/predict")
def predict(file: UploadFile):
    img = Image.open(file.file)
    pred = predict_img(model, img)

    title = get_title(pred)

    im_res = BytesIO()
    img = Image.fromarray(overlay_img(img, pred))
    img.save(im_res, "JPEG")

    res = base64.b64encode(im_res.getvalue())

    return {"title": title, "data": res}
