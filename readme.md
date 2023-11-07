<div align="center">

# Die-Cut Sticker GPT
<img src="https://github.com/kaneda2004/sticker_gpt/assets/4466807/47545897-525a-41f1-91ab-45dc625c9fec" width="30%">

</div>

<div align="left">
<!-- 
![20231107124503_e5afaf35-81a2-47d9-ab70-0f7a1fc7d171](https://github.com/kaneda2004/sticker_gpt/assets/4466807/47545897-525a-41f1-91ab-45dc625c9fec)
--!>

Make ultra high quality die cut stickers automatically with Die-Cut Sticker GPT! 🚀🖼✨

This sophisticated tool harnesses the power of OpenAI's API to generate vivid images from text prompts, meticulously removes backgrounds for that perfect sticker look, and employs Real-ESRGAN for crystal-clear upscaling.

## 🌟 Features

- **Prompt Refinement**: Leverage GPT-4's language model to transform your ideas into detailed prompts that produce stunning images. 📝✏️
- **DALL-E 3 Integration**: Create original images with the state-of-the-art DALL-E 3 model directly from refined prompts. 🎨👁
- **Background Removal**: Utilize `rembg` to seamlessly strip away backgrounds, leaving behind a clean, sticker-ready image. 🛠🌌
- **Alpha Matting**: Apply advanced alpha matting techniques to ensure edges are smooth and sticker-ready. 🖼👌
- **Image Upscaling**: Magnify image resolution by 4x with the power of Real-ESRGAN, making every detail pop. 🔍📈
- **Interactive Experience**: Engage with an intuitive command-line interface to guide you through the image generation process. 💻🤖


## Usage

To use Die-Cut Sticker GPT, follow these simple steps:

1. Begin by cloning the repository to your local system:
   ```
   git clone https://github.com/kaneda2004/StickerGPT
   ```
2. Navigate to the project directory:
   ```
   cd your-repository-name
   ```
3. Install the necessary dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set the `OPENAI_API_KEY` environment variable with your OpenAI API key. For Unix-based systems:
   ```
   export OPENAI_API_KEY='your_api_key'
   ```
   For Windows:
   ```
   set OPENAI_API_KEY=your_api_key
   ```
5. Execute the script:
   ```
   python main.py
   ```
6. Input your desired image description when prompted. The tool will refine the prompt and generate an image using DALL-E 3.
7. The script will then automatically remove the background to create a die-cut sticker look.
8. You'll be asked if you want to upscale the image using Real-ESRGAN. If you agree, the tool will enhance the image's resolution.
9. The final image will be saved in the specified directory. You'll then have the option to create another image or exit the program.

Enjoy creating high-quality stickers with ease!

## 📋 Requirements

- Python 3.x
- An OpenAI API key
- CUDA-enabled GPU for image upscaling

## 📄 License

This project is released under the [MIT License](LICENSE).

## 🙏 Acknowledgements

- Thanks to OpenAI for the API that empowers our image generation.
- Kudos to the `rembg` project for enabling precise background removal.
- A shoutout to the Real-ESRGAN project for their exceptional upscaling capabilities.
