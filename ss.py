import mss
import mss.tools
from pymongo import MongoClient
from datetime import datetime
import time
import base64

MONGO_URI = "MONGO DATABASE"
DATABASE_NAME = "DATABASE"
COLLECTION_NAME = "COLLECTION"
TEMP_IMAGE_FOLDER = "core_process"
if not os.path.exists(TEMP_IMAGE_FOLDER):
    os.makedirs(TEMP_IMAGE_FOLDER)

def capture_and_upload():
    try:
        with mss.mss() as sct:
            sct_img = sct.grab(sct.monitors[1])
            img_bytes = mss.tools.to_png(sct_img.rgb, sct_img.size)
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            timestamp = datetime.now()
            data = {
                "timestamp": timestamp,
                "image_base64": img_base64
            }
            client = MongoClient(MONGO_URI)
            db = client[DATABASE_NAME]
            collection = db[COLLECTION_NAME]
            collection.insert_one(data)
            print(f"Screenshot uploaded at {timestamp}")
            save_png(timestamp, img_base64)


    except Exception as e:
        print(f"Errore: {e}")

def save_png(timestamp, img_base64):
    try:
        filename = f"{TEMP_IMAGE_FOLDER}/screenshot_{timestamp.strftime('%Y%m%d%H%M%S%f')}.png"
        img_bytes = base64.b64decode(img_base64)
        with open(filename, "wb") as f:
           f.write(img_bytes)
        print(f"Image saved to {filename}")
    except Exception as e:
      print(f"ERROR: {e}")

def delete_png(filename):
    try:
      os.remove(filename)
      print(f"Image deleted from {filename}")
    except Exception as e:
      print(f"ERROR WHILE DELETING: {e}")

if __name__ == "__main__":
    while True:
        capture_and_upload()
        time.sleep(5)
