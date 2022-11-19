from flask import Flask, render_template, request
import numpy as np
from PIL import Image
import base64
import re
import io
import json
import torch
from PIL import Image

from diffusers import StableDiffusionImg2ImgPipeline
app = Flask(__name__)


# Prepare the Stable Diffusion Models in Flask
device = 'cuda' if torch.cuda.is_available() else 'mps'
model_id_or_path = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    model_id_or_path,
    revision="fp16", 
    torch_dtype=torch.float16,
)
pipe = pipe.to(device)


@app.route("/")
def home():
    return render_template('home.html')
    
@app.route('/load')
def load():
    return render_template('loading.html')

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    print ("generating image")
    return ("nothing")

@app.route('/hook', methods=['POST'])
def get_image():
    image_data = re.sub('^data:image/.+;base64,', '', request.form['imageBase64'])
    image_PIL = Image.open(io.BytesIO(base64.b64decode(image_data)))
    image_np = np.array(image_PIL)
    # print(image_np.shape)

    new_image = Image.new("RGBA", image_PIL.size, "WHITE") # Create a white rgba background
    new_image.paste(image_PIL, (0, 0), image_PIL)              # Paste the image on the background. Go to the links given below for details.
    new_image.convert('RGB').save('temp/canvas.jpeg', "JPEG") 
    prompt = request.form['prompt']
    strength = float(request.form['strength'])
    guidance_scale = float(request.form['guidance_scale'])
    generate_image_with_prompt(prompt, strength, guidance_scale)
    
    return json.dumps({'result': 'success'}), 200, {'ContentType': 'application/json'}


def generate_image_with_prompt(prompt, strength=0.75, guidance_scale=7.5):
    basewidth = 512
    img = Image.open('temp/canvas.jpeg')
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    init_image = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)

    images = pipe(prompt=prompt, init_image=init_image, strength=strength, guidance_scale=guidance_scale).images
    print(len(images))

    images[0].save("temp/generated.png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)