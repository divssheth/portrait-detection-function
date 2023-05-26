import azure.functions as func
import logging
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import json

app = func.FunctionApp()

# Learn more at aka.ms/pythonprogrammingmodel

# Get started by running the following code to create a function using a HTTP trigger.
@app.function_name(name="HttpTrigger1")
@app.route(route="validate")
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
    try:
        key = os.getenv("AZURE_COGNITIVE_SERVICE_KEY")
        region = os.getenv("AZURE_COGNITIVE_SERVICE_REGION")
        req_body = req.get_json()
        image_url = req_body["image_url"]

        credentials = CognitiveServicesCredentials(key)
        client = ComputerVisionClient(
            endpoint="https://" + region + ".api.cognitive.microsoft.com/",
            credentials=credentials,
        )

        # url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Broadway_and_Times_Square_by_night.jpg/450px-Broadway_and_Times_Square_by_night.jpg"

        image_analysis = client.analyze_image(
            image_url,
            visual_features=[VisualFeatureTypes.tags, VisualFeatureTypes.adult],
        )

        response = {}
        response["is_portrait"] = check_if_portrait(image_analysis)
        response["adult"] = process_adult_info(image_analysis)
        response["is_valid"] = determine_validity(response)
        return func.HttpResponse(
            json.dumps(response),
            mimetype="application/json",
            status_code=200
        )

    except Exception:
        return func.HttpResponse(
            f"Something went wrong, try again later", status_code=400
        )

def check_if_portrait(image_analysis):
    # Check if image is portrait
    portrait_tag = False
    for tag in image_analysis.tags:
        if tag.name == "portrait":
            portrait_tag = True
    return portrait_tag


def process_adult_info(image_analysis):
    adult = {}
    adult["is_gory_content"] = image_analysis.adult.is_gory_content
    adult["is_adult_content"] = image_analysis.adult.is_adult_content
    adult["is_racy_content"] = image_analysis.adult.is_racy_content
    adult["adult_score"] = image_analysis.adult.adult_score
    adult["racy_score"] = image_analysis.adult.racy_score
    adult["gore_score"] = image_analysis.adult.gore_score
    return adult


def determine_validity(response):
    is_valid = False
    if (
        (response["is_portrait"])
        and not (response["adult"]["is_adult_content"])
        and not (response["adult"]["is_racy_content"])
        and not (response["adult"]["is_gory_content"])
    ):
        is_valid = True
    return is_valid