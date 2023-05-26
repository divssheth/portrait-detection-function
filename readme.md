## Welcome to Image ID Validation
This Azure Function uses Computer Vision Version 3.2 API from Azure to detect if an image can be used on an ID. It also provides a score if the image has racy, adult, or gory content.

### Prerequisites
Before you can begin developing/testing locally, you will need to install [Azurite](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azurite?tabs=visual-studio) and set the following environment variables in the `local.settings.json` file:

- AZURE_COGNITIVE_SERVICE_KEY
- AZURE_COGNITIVE_SERVICE_REGION
- AZURE_COGNITIVE_SERVICE_NAME

You can find instructions on how to develop Azure Functions locally from the [Azure website](https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=python).

### Usage
To use the function, call the REST API (/api/validate) with a JSON body passing `image_url` as a key with the image URL.

Sample request body:
{
    "image_url": "URL"
}

Sample response body:
{
    "is_portrait": true,
    "adult": {
        "is_gory_content": true,
        "is_adult_content": false,
        "is_racy_content": false,
        "adult_score": 0.006854687351733446,
        "racy_score": 0.012399628758430481,
        "gore_score": 0.8282324075698853
    },
    "is_valid": false
}
