# Artisian
A project submitted to HackWestern 9.

### Getting started
```bash
pip install -r requirements.txt
```

The code runs on Flask, with a backend powered by a StableDiffusion model hosted on Hugging face. All of the compute is done locally, but you still need to login onto `huggingface-cli`.

They will ask you for a token, which you can obtain from here (after being logged in): https://www.huggingface.co/settings/tokens

Laucnh the Flask app by running `python3 main.py`

### Stable Diffusion
If you just want to play around with the Stable Diffusion models, run the following commands:
```
cd backend/
python3 main.py
```

You can specify the path of the image inside the `main.py` file.
