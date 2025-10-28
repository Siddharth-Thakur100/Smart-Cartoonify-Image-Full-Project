import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image

# Load model once
MODEL_HANDLE = "models/ai_style_model/"
model = hub.load(MODEL_HANDLE)

def load_image_pil(pil_img, max_dim=512):
    img = np.array(pil_img).astype(np.float32) / 255.0
    h, w = img.shape[:2]
    scale = max_dim / max(h, w)
    img = tf.image.resize(img, (int(h*scale), int(w*scale)))
    img = img[tf.newaxis, ...]
    return img

def ai_stylize(content_pil, style_pil):
    content = load_image_pil(content_pil)
    style = load_image_pil(style_pil)
    outputs = model(tf.constant(content), tf.constant(style))
    stylized = outputs[0][0].numpy()
    stylized = np.clip(stylized*255, 0, 255).astype('uint8')
    return stylized