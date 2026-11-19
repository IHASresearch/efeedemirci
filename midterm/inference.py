from pathlib import Path
import sys

import numpy as np
from PIL import Image
import torch

sys.path.insert(0, str(Path(__file__).parent / 'data' / 'pix2pix_kaynak' / 'models'))
import networks


def image_to_tensor(image, size=512):
    image = image.convert('RGB').resize((size, size), Image.Resampling.BICUBIC)
    array = np.asarray(image, dtype=np.float32) / 127.5 - 1.0
    return torch.from_numpy(array.transpose(2, 0, 1)).unsqueeze(0)


def tensor_to_image(tensor):
    array = tensor.detach().cpu().float().numpy()[0].transpose(1, 2, 0)
    array = ((array + 1) / 2 * 255).clip(0, 255).astype(np.uint8)
    return Image.fromarray(array)


def load_model(path):
    model = networks.define_G(3, 3, 64, 'unet_256', 'batch', True)
    weights = torch.load(path, map_location='cpu', weights_only=True)
    model.load_state_dict(weights, strict=True)
    model.eval()
    return model


def predict(model, image):
    with torch.inference_mode():
        return tensor_to_image(model(image_to_tensor(image)))
