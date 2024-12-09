import requests
import gradio as gr
from PIL import Image, ImageDraw, ImageFont
import random
import io
import platform

# Features for Vision API
FEATURES = ["read", "smartCrops", "tags", "people", "caption", "denseCaptions", "objects"]
LANGUAGE_CODE = "en"

def request_background_removal(mode="backgroundRemoval", image_path=""):
    """
    Send an image to Azure API for background removal.
    """
    endpoint = "your_background_removal_endpoint"  # Replace with your endpoint
    params = {
        "api-version": "2023-04-01-preview",
        "mode": mode
    }
    headers = {
        "Ocp-Apim-Subscription-Key": "your_subscription_key",  # Replace with your key
        "Content-Type": "application/octet-stream"
    }
    
    with open(image_path, "rb") as image:
        image_data = image.read()
    
    response = requests.post(endpoint, params=params, headers=headers, data=image_data)
    print(response.status_code)
    
    if response.status_code == 200:        
        return response.content
    else:
        return None

def request_vision(feature_list=["objects"], image_path="", smartcrops_value=None):
    """
    Send an image to Azure API for vision analysis.
    """
    endpoint = "your_vision_analysis_endpoint"  # Replace with your endpoint
    params = {
        "language": LANGUAGE_CODE,
        "gender-neutral-caption": "false",
        "api-version": "2023-10-01",
        "features": ",".join(feature_list)
    }
    headers = {
        "Ocp-Apim-Subscription-Key": "your_subscription_key",  # Replace with your key
        "Content-Type": "application/octet-stream"
    }
    
    with open(image_path, "rb") as image:
        image_data = image.read()
    
    if smartcrops_value:
        params.update({"smartcrops-aspect-ratios": smartcrops_value})
    
    response = requests.post(endpoint, params=params, headers=headers, data=image_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": response.status_code, "message": response.text}

def random_color():
    """Generate a random RGB color."""
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def draw_image(feature_list, image_path, response_json):
    """
    Draw bounding boxes and annotations on the image based on API response.
    """
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    font_size = 10
    if platform.system() == "Darwin":
        font = ImageFont.truetype("AppleGothic.ttf", size=font_size)
    elif platform.system() == "Windows":
        font = ImageFont.truetype("malgun.ttf", size=font_size)
    else:
        font = ImageFont.load_default()
    
    for feature in feature_list:
        result_key = f"{feature}Result"
        result_object = response_json[result_key]
        color = random_color()
        
        if "values" in result_object:
            values = result_object['values']
            for value in values:
                if "boundingBox" in value:
                    bounding_box = value["boundingBox"]
                    x, y, w, h = bounding_box['x'], bounding_box['y'], bounding_box['w'], bounding_box['h']
                    draw.rectangle([(x, y), (x + w, y + h)], outline=color, width=2)
        elif "blocks" in result_object:
            block_list = result_object["blocks"]
            for block in block_list:
                line_list = block['lines']
                for line in line_list:
                    text = line["text"]
                    bounding_polygon = line["boundingPolygon"]
                    polygon = [(p["x"], p["y"]) for p in bounding_polygon]
                    draw.polygon(polygon, outline=color, fill=None, width=2)
                    draw.text((bounding_polygon[3]['x'], bounding_polygon[3]['y'] + 3), 
                              text=text, fill=color, font=font)
    return image

def change_image(feature_list, image_path, smartcrops_value):
    """
    Analyze an image and return the processed result.
    """
    if len(feature_list) == 0 or not image_path:
        return None, None
    
    if "smartCrops" not in feature_list:
        smartcrops_value = None
    
    response_json = request_vision(feature_list=feature_list, 
                                   image_path=image_path, 
                                   smartcrops_value=smartcrops_value)
    image = draw_image(feature_list, image_path, response_json)
    return response_json, image

def change_background_image(removal_type, image_path):
    """
    Process an image for background removal.
    """
    image_data = request_background_removal(mode=removal_type, image_path=image_path)
    if image_data:
        return Image.open(io.BytesIO(image_data))
    return None

with gr.Blocks() as demo:
    smartcrops_value = gr.State("")
    
    with gr.Tab("Image Analysis"):
        language_radio = gr.Radio(label="Language", choices=["en", "ko"], value="en")
        features_checkbox = gr.CheckboxGroup(label="Features", choices=FEATURES)
        input_image = gr.Image(label="Input Image", type="filepath")
        result_image = gr.Image(label="Result Image", type="pil", interactive=False)
        result_json = gr.JSON(label="Result JSON")
        
        input_image.change(fn=change_image, 
                           inputs=[features_checkbox, input_image, smartcrops_value], 
                           outputs=[result_json, result_image])
    
    with gr.Tab("Background Removal"):
        removal_type_radio = gr.Radio(label="Removal Type", choices=["backgroundRemoval", "foregroundMatting"], value="backgroundRemoval")
        input_background_image = gr.Image(label="Input Image", type="filepath")
        result_background_image = gr.Image(label="Result Image", type="pil", interactive=False)
        
        input_background_image.change(fn=change_background_image, 
                                      inputs=[removal_type_radio, input_background_image], 
                                      outputs=[result_background_image])

demo.launch()