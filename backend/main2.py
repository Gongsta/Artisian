# TODO: https://github.com/LambdaLabsML/lambda-diffusers

from pathlib import Path
from lambda_diffusers import StableDiffusionImageEmbedPipeline
from PIL import Image
import torch
device = "cuda" if torch.cuda.is_available() else "mps"
pipe = StableDiffusionImageEmbedPipeline.from_pretrained("lambdalabs/sd-image-variations-diffusers")
pipe = pipe.to(device)

img = Image.open("../static/canvas.jpeg")
basewidth = 512
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
im = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)
num_samples = 10
image = pipe(num_samples*[im], guidance_scale=3.0)
image = image["sample"]
base_path = Path("outputs/im2im")
base_path.mkdir(exist_ok=True, parents=True)
for idx, im in enumerate(image):
    im.save(base_path/f"{idx:06}.jpg")