import cv2
import numpy as np
from PIL import Image
import requests
import os


def download_model():
    """Download the model if it doesn't exist"""
    model_url = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
    model_path = "RealESRGAN_x4plus.pth"

    if not os.path.exists(model_path):
        print("Downloading model...")
        response = requests.get(model_url)
        with open(model_path, 'wb') as f:
            f.write(response.content)
        print("Model downloaded!")
    return model_path


def enhance_image_simple(input_path, output_path, scale=2):
    """Simple enhancement without problematic dependencies"""

    # Read image
    img = cv2.imread(input_path)

    # Method 1: Advanced OpenCV enhancement
    # Noise reduction
    denoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

    # Edge-preserving filter
    smooth = cv2.edgePreservingFilter(denoised, flags=1, sigma_s=150, sigma_r=0.25)

    # Sharpening
    gaussian_3 = cv2.GaussianBlur(smooth, (0, 0), 2.0)
    unsharp_mask = cv2.addWeighted(smooth, 1.5, gaussian_3, -0.5, 0)

    # High-quality upscaling
    height, width = unsharp_mask.shape[:2]
    upscaled = cv2.resize(unsharp_mask, (width * scale, height * scale),
                          interpolation=cv2.INTER_LANCZOS4)

    # Final sharpening
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    final = cv2.filter2D(upscaled, -1, kernel)

    cv2.imwrite(output_path, final)
    return final


# Usage (requires installing real-esrgan)
# pip install realesrgan
upscaled_img = enhance_image_simple('generated_image_24c50410-1ea7-47fb-bbf8-c8aba57ba30b.png', 'enhanced_output.jpg', scale=2)