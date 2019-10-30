import requests
import base64
import argparse
import subprocess


def classify_deployed(file_name):
    payload = None
    with open(file_name, 'rb') as f:
        payload = f.read()
        payload = bytearray(payload)

    return payload

# Coffee,Coffee Cup,Raspberry Pie,Timmy,Water Bottle
labels = ['Coffee', 'Coffee Cup', 'Marker', 'Raspberry Pie', 'Timmy','Water Bottle']
voice = {
    labels[0]: "/Users/patryan/Development/mygithub/aws-ml-vision/mp3s/speech_coffee_mug.mp3",
    labels[1]: "/Users/patryan/Development/mygithub/aws-ml-vision/mp3s/speech_coffee_cup_recycle.mp3",
    labels[2]: "/Users/patryan/Development/mygithub/aws-ml-vision/mp3s/speech_marker.mp3",
    labels[3]: "/Users/patryan/Development/mygithub/aws-ml-vision/mp3s/speech_rpi.mp3",
    labels[4]: "/Users/patryan/Development/mygithub/aws-ml-vision/mp3s/speech_timmy.mp3",
    labels[5]: "/Users/patryan/Development/mygithub/aws-ml-vision/mp3s/speech_water_bottle.mp3"
}

def play_audio(predicted_label):
    print(f"Play: {predicted_label}")
    audio_file = voice[predicted_label]

    return_code = subprocess.call(["afplay", audio_file])

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
    status_code = response_json['statusCode']
    predicted_label = response_json['body']['predicted_label']
    print(f"Status Code: {response_json['statusCode']}")
    print(f"Predicted Label: {response_json['body']['predicted_label']}")
    print(f"Predicted Probability: {response_json['body']['predicted_probability']}")
    print("")
    print(f"All Predictions: {response_json['body']['predictions']}")
    print("-------------------")

    if status_code == 200:
        play_audio(predicted_label)
