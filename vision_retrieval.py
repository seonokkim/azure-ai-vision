import requests
from IPython.display import JSON

# Replace with your Azure Vision API details
base_url = "your_base_url"  # Example: "https://your-resource-name.cognitiveservices.azure.com/"
api_key = "your_api_key"
index_name = "your_index_name"

# Endpoint for creating or updating the index
endpoint = f"{base_url}computervision/retrieval/indexes/{index_name}?api-version=2023-05-01-preview"

headers = {
    "Ocp-Apim-Subscription-Key": api_key,
    "Content-Type": "application/json"
}

# Payload to define the metadata schema and features
payload = {
    'metadataSchema': {
        'fields': [
            {
                'name': 'cameraId',
                'searchable': False,
                'filterable': True,
                'type': 'string'
            },
            {
                'name': 'timestamp',
                'searchable': False,
                'filterable': True,
                'type': 'datetime'
            }
        ]
    },
    'features': [
        {
            'name': 'vision',
            'domain': 'surveillance'
        },
        {
            'name': 'speech'
        }
    ]
}

# Create or update the index
response = requests.put(endpoint, headers=headers, json=payload)
print("Create/Update Index:", response.status_code, response.text)

# Endpoint for adding videos to the index
ingestion_id = "your_ingestion_id"  # Replace with a unique ingestion ID
endpoint2 = f"{base_url}computervision/retrieval/indexes/{index_name}/ingestions/{ingestion_id}?api-version=2023-05-01-preview"

# Payload for adding a video
payload2 = {
    'videos': [
        {
            'mode': 'add',
            'documentId': 'your_document_id',  # Replace with a unique document ID
            'documentUrl': 'your_document_url',  # Replace with the video URL in your storage
            'metadata': {
                'cameraId': 'camera1',
                'timestamp': '2023-06-30 17:40:33'
            }
        }
    ]
}

# Add video to the index
response = requests.put(endpoint2, headers=headers, json=payload2)
print("Add Video:", response.status_code, response.text)

# Endpoint for listing ingestions
endpoint3 = f"{base_url}computervision/retrieval/indexes/{index_name}/ingestions?api-version=2023-05-01-preview&$top=20"

# List ingestions
response = requests.get(endpoint3, headers=headers)
print("List Ingestions:", response.status_code)
if response.status_code == 200:
    ingestions = response.json()
    print("Ingestions:", ingestions)

# Endpoint for querying the index by text
endpoint4 = f"{base_url}computervision/retrieval/indexes/{index_name}:queryByText?api-version=2023-05-01-preview"

# Payload for querying the index
payload4 = {
    'queryText': 'vehicle',
    'filters': {
        'stringFilters': [
            {
                'fieldName': 'cameraId',
                'values': [
                    'camera1'
                ]
            }
        ],
        'featureFilters': ['vision']
    }
}

# Query the index
response = requests.post(endpoint4, headers=headers, json=payload4)
print("Query Index by Text:", response.status_code)
if response.status_code == 200:
    response_json = response.json()
    JSON(response_json)  # Display the JSON response