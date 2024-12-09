from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os
import time

# Replace with your Azure Custom Vision resource details
training_endpoint = "your_training_endpoint"
prediction_endpoint = "your_prediction_endpoint"

training_key = "your_training_key"
prediction_key = "your_prediction_key"
prediction_resource_id = "your_prediction_resource_id"

# Azure Custom Vision client credentials
training_credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})

# Create training and prediction clients
trainer = CustomVisionTrainingClient(endpoint=training_endpoint, credentials=training_credentials)
predictor = CustomVisionPredictionClient(endpoint=prediction_endpoint, credentials=prediction_credentials)

# List existing projects
for project in trainer.get_projects():
    print(project.id, project.name)

# List available domains
for domain in trainer.get_domains():
    print(domain.type, domain.name, domain.id)

# Project configuration
project_name = "custom-vision-project"
description = "Model to detect fork and scissors"
domain_id = None

# Check for existing project
has_project = False
project_id = None

for existing_project in trainer.get_projects():
    if existing_project.name == project_name:
        project_id = existing_project.id
        has_project = True
        break

# Select the object detection domain
for domain in trainer.get_domains():
    if domain.type == "ObjectDetection" and domain.name == "General":
        domain_id = domain.id
        break

# Create or retrieve the project
if domain_id:
    if has_project:
        print("Existing project found.")
        project = trainer.get_project(project_id=project_id)
    else:
        print("Creating a new project.")
        project = trainer.create_project(project_name, description, domain_id)

print(project.id, project.name)

# Check for existing tags
existing_tags = trainer.get_tags(project_id=project.id)
fork_tag = None
scissors_tag = None

for tag in existing_tags:
    if tag.name == "fork":
        print("Fork tag found.")
        fork_tag = tag
    elif tag.name == "scissors":
        print("Scissors tag found.")
        scissors_tag = tag

# Create tags if not found
if fork_tag is None:
    print("Creating fork tag.")
    fork_tag = trainer.create_tag(project_id=project.id, name="fork")
if scissors_tag is None:
    print("Creating scissors tag.")
    scissors_tag = trainer.create_tag(project_id=project.id, name="scissors")

print(fork_tag)
print(scissors_tag)

# Regions for each image
fork_image_regions = {
    "fork_1": [0.145833328, 0.3509314, 0.5894608, 0.238562092],
    # Add other fork regions here...
}

scissors_image_regions = {
    "scissors_1": [0.4007353, 0.194068655, 0.259803921, 0.6617647],
    # Add other scissors regions here...
}

# Prepare images with regions
tagged_images_with_regions = []

# Add fork images
for file_name, region_coords in fork_image_regions.items():
    x, y, w, h = region_coords
    regions = [Region(tag_id=fork_tag.id, left=x, top=y, width=w, height=h)]
    with open(os.path.join("./images/fork", f"{file_name}.jpg"), 'rb') as image:
        image_data = image.read()
    tagged_images_with_regions.append(ImageFileCreateEntry(name=file_name, contents=image_data, regions=regions))

# Add scissors images
for file_name, region_coords in scissors_image_regions.items():
    x, y, w, h = region_coords
    regions = [Region(tag_id=scissors_tag.id, left=x, top=y, width=w, height=h)]
    with open(os.path.join("./images/scissors", f"{file_name}.jpg"), 'rb') as image:
        image_data = image.read()
    tagged_images_with_regions.append(ImageFileCreateEntry(name=file_name, contents=image_data, regions=regions))

# Upload images with regions
upload_result = trainer.create_images_from_files(project_id=project.id, batch=ImageFileCreateBatch(images=tagged_images_with_regions))

print("Number of images uploaded:", len(tagged_images_with_regions))
if upload_result.is_batch_successful:
    print("Image upload succeeded.")
else:
    for image in upload_result.images:
        print("Image upload status:", image.status)

# Train the project
existing_iterations = trainer.get_iterations(project_id=project.id)
if existing_iterations:
    iteration = existing_iterations[0]
else:
    iteration = trainer.train_project(project_id=project.id)

# Wait for training to complete
while iteration.status != "Completed":
    iteration = trainer.get_iteration(project.id, iteration.id)
    print("Training status:", iteration.status)
    time.sleep(3)

print("Training completed.")

# Publish the iteration
publish_name = "object-detection-v1"
trainer.publish_iteration(project_id=project.id, iteration_id=iteration.id, publish_name=publish_name, prediction_id=prediction_resource_id)
print("Iteration published:", publish_name)