import requests
import torch
from PIL import Image
from io import BytesIO

from diffusers import StableDiffusionImg2ImgPipeline

# load the pipeline
# device = 'cuda' if torch.cuda.is_available() else 'cpu'
device = "mps" # for M1 Mac
model_id_or_path = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    model_id_or_path,
    revision="fp16", 
    torch_dtype=torch.float16,
)

pipe = pipe.to("mps")

# # let's download an initial image
# url = "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/img2img/sketch-mountains-input.jpg"

# response = requests.get(url)
# init_image = Image.open(BytesIO(response.content)).convert("RGB")
# init_image = init_image.resize((768, 512))
basewidth = 512
img = Image.open('test.jpeg')
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
init_image = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)

prompt = "A fantasy landscape, trending on artstation"
# prompt = "Something weird"

images = pipe(prompt=prompt, init_image=init_image, strength=0.75, guidance_scale=7.5).images
print(len(images))

images[0].save("fantasy_landscape.png")