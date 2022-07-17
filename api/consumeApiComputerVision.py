'''
pip install --upgrade azure-cognitiveservices-vision-computervision
pip install pillow
'''
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
import sys
import time
import re


def consumeApiComputerVision():
    subscription_key = "1e1089ba90d34382a703ccb3f582ad5e"
    endpoint = "https://cv-proyectogrado.cognitiveservices.azure.com/"

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    print("===== Read File - remote =====")    
    read_image_url = "https://practicatest.co/static/img/posts/co/historial-auto-placa-matricula.jpg"
    read_response = computervision_client.read(read_image_url,  raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    # Print the detected text, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                if re.search("[a-zA-Z]{3}.[0-9]{2}[a-zA-Z0-9]", line.text):
                    return line.text, line.bounding_box
        return "No se pudo procesar la placa :c", "666"

if __name__ == '__main__':
    s,d = consumeApiComputerVision()
    print(s)