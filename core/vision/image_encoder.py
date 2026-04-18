import base64
import io
from PIL import Image
from utils.logger import logger

def encode_image_to_base64(image_bytes:bytes)->str:
    return base64.b64encode(image_bytes).decode("utf-8")

def resize_if_needed(
        image_bytes:bytes,
        max_size:int=1024,
)-> bytes:
    img=Image.open(io.BytesIO(image_bytes))
    w,h=img.size

    if max(w,h)>max_size:
        ratio=max_size/max(w,h)
        new_size=(int(w*ratio),int(h*ratio))
        img=img.resize(new_size,Image.LANCZOS)
        logger.info(f"Image resized:{w}x{h}->{new_size[0]}x{new_size[1]}")
    else:
        logger.debug(f"Image size OK-no resize needed:{w}x{h}")

    buf=io.BytesIO()
    img.save(buf,format="JPEG",quality=85)
    return buf.getvalue()

def prepare_image(image_bytes:bytes)->str:
    resized=resize_if_needed(image_bytes)
    encoded=encode_image_to_base64(resized)
    logger.debug(f"Image preoared - base64 length:{len(encoded)}")
    