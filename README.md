# Azure AI Vision

This repository demonstrates the integration of Azure AI Vision services for tasks such as custom vision training, image analysis, and vision retrieval. The examples include practical Python scripts to work with Azure Cognitive Services for object detection, image processing, and video indexing.

## Features

- **Custom Vision Training**: Train a custom vision model using Azure's Custom Vision service.
- **Image Analysis**: Perform tasks like object detection, captioning, and smart crops with Azure Computer Vision API.
- **Vision Retrieval**: Manage and query indexes for video and image-based metadata using Azure Vision Retrieval APIs.

## Repository Structure

```plaintext
.
├── custom_vision_training.py   # Script for training a custom vision model
├── custom_vision.py            # Script for interacting with trained custom vision models
├── image_analysis.py           # Script for analyzing images with Azure AI
├── vision_retrieval.py         # Script for creating and querying vision retrieval indexes
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
```

## Prerequisites

Before using the scripts, ensure the following:

1. **Azure Subscription**: You must have an active Azure subscription.

2. **Azure Cognitive Services**: Create Azure resources for the following services:
   - **Custom Vision**: Used for training and deploying custom object detection models.
   - **Computer Vision**: Used for image analysis tasks such as object detection, captioning, and smart crops.
   - **Vision Retrieval**: Used for indexing and querying video and image-based metadata.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/azure-ai-vision.git
   cd azure-ai-vision
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Custom Vision Training
Use the `custom_vision_training.py` script to train a custom object detection model.

- **Steps**:
  1. Replace placeholders in the script (`your_training_endpoint`, `your_training_key`, etc.) with your Azure Custom Vision resource details.
  2. Organize your images in the specified directories (e.g., `images/fork`, `images/scissors`).
  3. Run the script:
     ```bash
     python custom_vision_training.py
     ```

### 2. Custom Vision Model Interaction
Use the `custom_vision.py` script to interact with a deployed custom vision model. This script sends images to the model for prediction.

- **Steps**:
  1. Replace placeholders with your Custom Vision prediction endpoint and key.
  2. Run the script:
     ```bash
     python custom_vision.py
     ```

### 3. Image Analysis
Use the `image_analysis.py` script to perform image analysis tasks like object detection, caption generation, and smart crops.

- **Steps**:
  1. Replace placeholders with your Azure Computer Vision API details.
  2. Run the script:
     ```bash
     python image_analysis.py
     ```

### 4. Vision Retrieval
Use the `vision_retrieval.py` script to manage and query indexes for image and video metadata.

- **Steps**:
  1. Replace placeholders (`your_base_url`, `your_api_key`, etc.) with your Vision Retrieval API details.
  2. Run the script:
     ```bash
     python vision_retrieval.py
     ```

## Configuration

For each script, replace placeholders with your Azure Cognitive Services credentials:

- **Custom Vision**:
  - `your_training_endpoint`
  - `your_training_key`
  - `your_prediction_endpoint`
  - `your_prediction_key`
- **Computer Vision**:
  - `your_base_url`
  - `your_api_key`
- **Vision Retrieval**:
  - `your_index_name`
  - `your_document_url`

Ensure that your images and videos are accessible from the specified paths.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Azure Custom Vision](https://learn.microsoft.com/en-us/azure/cognitive-services/custom-vision/)
- [Azure Computer Vision](https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/)
- [Azure Vision Retrieval](https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/concept-vision-retrieval)
