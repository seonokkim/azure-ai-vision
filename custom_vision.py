import gradio as gr
from PIL import Image, ImageDraw, ImageFont
import platform
import random
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

# Replace with your Azure Custom Vision information
prediction_endpoint = "your_endpoint"
prediction_key = "your_prediction_key"

# Azure Custom Vision credentials
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(endpoint=prediction_endpoint, credentials=prediction_credentials)

# Replace with your project details
project_id = "your_project_id"
publish_name = "your_publish_name"

def request_custom_vision(image_path):
    """
    Send an image to Azure Custom Vision for prediction.
    """
    with open(image_path, "rb") as image:
        image_data = image.read()
    response = predictor.detect_image(project_id=project_id, published_name=publish_name, image_data=image_data)
    return response.predictions

def random_color():
    """
    Generate a random RGB color.
    """
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def draw_image(image_path, predictions):
    """
    Draw bounding boxes and labels on the image based on predictions.
    """
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    print("Image size:", image_width, image_height)

    font_size = 15
    if platform.system() == "Darwin":
        font = ImageFont.truetype("AppleGothic.ttf", size=font_size)
    elif platform.system() == "Windows":
        font = ImageFont.truetype("malgun.ttf", size=font_size)
    else:
        font = ImageFont.load_default()

    for prediction in predictions:
        if prediction.probability > 0.5:
            probability = prediction.probability * 100
            tag_name = prediction.tag_name
            text = "{}({:.2f}%)".format(tag_name, probability)

            bounding_box = prediction.bounding_box
            left = bounding_box.left * image_width
            top = bounding_box.top * image_height
            width = bounding_box.width * image_width
            height = bounding_box.height * image_height

            color = random_color()
            draw.rectangle((left, top, left + width, top + height), outline=color, width=2)
            draw.text((left + 5, top + 5), text=text, fill=color, font=font)
            print("Prediction:", text, "Location:", left, top, width, height)

    return image

def upload_image(image_path):
    """
    Handle image upload, make predictions, and return the annotated image.
    """
    predictions = request_custom_vision(image_path)
    image = draw_image(image_path, predictions)
    return image

with gr.Blocks() as demo:
    input_image = gr.Image(type="filepath", label="Upload Image")
    output_image = gr.Image(type="pil", label="Result Image")

    input_image.upload(fn=upload_image, inputs=[input_image], outputs=[output_image])

demo.launch()