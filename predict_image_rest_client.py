import requests
import base64
import argparse

def classify_deployed(file_name):
    payload = None
    with open(file_name, 'rb') as f:
        payload = f.read()
        payload = bytearray(payload)

    return payload


labels = ['Cat', 'Dog', 'Ernest T Bass', 'Panda', 'Water Bottle']

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--image-path", type=str, required=True, help="path and name of the image")
    ap.add_argument("--api-gateway-url", type=str, required=True, help="API Gateway url talking to the prediction lambda")

    args = vars(ap.parse_args())
    image_path = args['image_path']
    api_gateway_url = args['api_gateway_url']

    payload_body = classify_deployed(image_path)

    payload_body = base64.b64encode(payload_body).decode()
    payload = {
        'data': payload_body
    }
    response = requests.post(api_gateway_url, data=None, json=payload)

    response_json = response.json()
    print(f"Status Code: {response_json['statusCode']}")
    print(f"Predicted Label: {response_json['body']['predicted_label']}")
    print(f"Predicted Probability: {response_json['body']['predicted_probability']}")
    print("")
    print(f"All Predictions: {response_json['body']['predictions']}")
    print("-------------------")
