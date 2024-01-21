import requests
import io
import numpy as np
from PIL import Image

JAVAPI = "http://5318-122-11-177-28.ngrok-free.app"


def download_images(script):
    queries = []
    for scene in script["scenes"]:
        queries.append(scene["image"])
    paths = requests.post(f"{JAVAPI}/search_images", json={"queries": queries}).json()[
        "result"
    ]
    images = []
    for path in paths:
        image_string = requests.get(f"{JAVAPI}/get_image", json={"image": path}).content
        img = Image.open(io.BytesIO(image_string))
        arr = np.array(img.resize((720, 640)))
        images.append(arr)
    return images
