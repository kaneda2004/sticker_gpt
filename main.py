# Import necessary libraries and modules
from openai import OpenAI
import os
from rembg import remove
from PIL import Image
import requests
from io import BytesIO
import uuid
from datetime import datetime
from termcolor import colored
import numpy as np
from realesrgan.utils import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet

# Retrieve the OpenAI API key from the environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client
client = OpenAI()

# Initialize the upsampler for images with the specified parameters
upsampler = RealESRGANer(
    scale=4, 
    device='cuda', 
    gpu_id=0, 
    model=RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4),
    model_path='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth'
)

# Define a function to refine the user's prompt for better results from DALL-E
# Define a function to refine the user's prompt for better results from DALL-E
def refine_prompt(prompt):
    # Send the prompt to OpenAI's chat model for refinement
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            # System message to set the context for the AI
            {
                "role": "system",
                "content": "Your task is to refine the user prompt. The user is requesting an image to be made with Dall E 3, improve the prompt in order to get excellent results with dalle. The image MUST be a die-cut sticker. Only reply with the prompt - nothing else. Remember it MUST be a die cut sticker (white border)."
            },
            # The user's original prompt
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
    )
    # Extract and return the content of the message from the response
    refined_content = response.choices[0].message.content
    print(colored(f"\nRefined Prompt: {refined_content}\n", 'yellow'))
    return refined_content

# Define a function to generate an image based on the refined prompt
def generate_image(prompt):
    try:
        # Use OpenAI's API to generate an image from the prompt
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        # Extract the URL of the generated image
        image_url = response.data[0].url
        return image_url
    except Exception as error:
        # Print any errors that occur during image generation
        print(f"Error: {error}")
        return None
    
# Function to upscale the image with RealESRGAN
def upscale_image(filename):
    input_path = f'images/{filename}'
    img = Image.open(input_path)
    # Upscale the image using RealESRGAN
    upscaled_image_np, _ = upsampler.enhance(np.array(img))
    # Convert the upscaled image back to PIL Image
    upscaled_image = Image.fromarray(upscaled_image_np)
    # Save the upscaled image with the new filename
    upscaled_filename = f'4x_{filename}'
    upscaled_image.save(f'images/{upscaled_filename}')
    return upscaled_filename

# Function to save the image to disk, remove the background, and apply alpha matting
def save_and_remove_background(image_url):
    # Create the images/ directory if it doesn't exist
    os.makedirs("images/", exist_ok=True)
    # Get the image from the URL and open it
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Use rembg to remove the background from the image with alpha matting parameters
    img_nobg_np = remove(
        np.array(img),
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=12
    )

    # Convert NumPy array back to PIL Image
    img_nobg = Image.fromarray(img_nobg_np)

    # Generate a unique filename for the image without background
    filename = f'{datetime.now().strftime("%Y%m%d%H%M%S")}_{uuid.uuid4()}.png'
    # Save the image without background to the 'images/' directory
    img_nobg.save(f'images/{filename}')
    return filename


# Main loop to interact with the user
while True:
    user_prompt = input("Enter your prompt: ")
    refined_prompt = refine_prompt(user_prompt)
    
    while True:  # Loop for re-generating or generating new images
        image_url = generate_image(refined_prompt)
        if image_url:
            filename = save_and_remove_background(image_url)
            print(f"Image saved and background removed as {filename}")
            
            # Ask the user if they want to upscale the image
            upscale_choice = input("Do you want to upscale the image 4x with RealESRGAN? (yes/no): ").lower()
            if upscale_choice in ['yes', 'y']:
                upscaled_filename = upscale_image(filename)
                print(f"Image upscaled and saved as {upscaled_filename}")
            else:
                print(f"Image saved as {filename} without upscaling.")

        # Ask the user if they want to re-generate the image with the same prompt or use a new prompt
        regen_choice = input("Do you want to re-generate the image with the same prompt, enter a new prompt, or exit? (re-generate/NEW/EXIT | r/n/e): ").lower()
        if regen_choice in ['new', 'n']:
            break  # Exit to the outer loop to get a new prompt
        elif regen_choice in ['exit', 'e']:
            exit()  # Exit the program
        elif regen_choice not in ['re-generate', 'r']:
            print("Invalid choice. Please enter 're-generate', 'NEW', 'EXIT', 'n', or 'e'.")
