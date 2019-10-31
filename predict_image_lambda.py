import os
import io
import boto3
import json
import csv
import operator
import base64

"""
Set the following environment variables in the lambda

ENDPOINT_NAME  recycle-guru-endpoint


LABELS  Coffee,Coffee Cup,Marker,Raspberry Pie,Timmy,Water Bottle


"""

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME'] if 'ENDPOINT_NAME' in os.environ else 'recycle-guru-endpoint'

session = boto3.Session()
client = session.client("sagemaker-runtime", region_name='us-east-1')

labels = ['Coffee', 'Water Bottle']
if 'LABELS' in os.environ:
    label_str = os.environ['LABELS']
    labels = label_str.split(",")

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    data = json.loads(json.dumps(event))
    payload = data['data']
    payload = base64.b64decode(payload)

    response = client.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        Body=payload,
        ContentType='application/x-image'
    )

    predictions = json.loads(response['Body'].read())

    print(predictions)

    max_index, max_value = max(enumerate(predictions), key=operator.itemgetter(1))

    predicted_label = labels[max_index]

    return {
        'statusCode': 200,
        'body': {
            'predicted_label': predicted_label,
            'predicted_probability': max_value,
            'predictions': [(labels[i],p) for i, p in enumerate(predictions)]
        }
    }



if __name__ == '__main__':
    def classify_deployed(file_name):
        payload = None
        with open(file_name, 'rb') as f:
            payload = f.read()
            payload = bytearray(payload)

        return payload


    test_images = [
        (labels[0],
         '/Users/patryan/Development/mybitbucket/sagemaker-image-classifier/data/data_resize_224_224/cats/cats_00009.jpg'),
        (labels[1],
         '/Users/patryan/Development/mybitbucket/sagemaker-image-classifier/data/data_resize_224_224/dogs/dogs_00024.jpg'),
        (labels[2],
         '/Users/patryan/Development/mybitbucket/sagemaker-image-classifier/data/data_resize_224_224/ernest_t_bass/ernest_t_bass_SH7lK.png'),
        (labels[3],
         '/Users/patryan/Development/mybitbucket/sagemaker-image-classifier/data/data_resize_224_224/panda/panda_00024.jpg'),
        (labels[4],
         '/Users/patryan/Development/mybitbucket/sagemaker-image-classifier/data/data_resize_224_224/water_bottle/water_bottle_1Cgdy.png')
    ]

    for test_label, test_image in test_images:

        payload_body = classify_deployed(test_image)

        event = {
            'data': base64.b64encode(payload_body).decode()
        }

        res = lambda_handler(event, None)
        print(res)

