import requests
import base64
import argparse
import boto3
import os

defaultRegion = 'us-east-1'
defaultUrl = 'https://polly.us-east-1.amazonaws.com'
profile_name = None


def connectToPolly(regionName=defaultRegion, endpointUrl=defaultUrl):
    return boto3.client('polly', region_name=regionName, endpoint_url=endpointUrl)


def speak(polly, text, format='mp3', voice='Joanna'):
    resp = polly.synthesize_speech(OutputFormat=format, Text=text, VoiceId=voice)
    soundfile = open('./tmp/sound.mp3', 'wb')
    soundBytes = resp['AudioStream'].read()
    soundfile.write(soundBytes)
    soundfile.close()
    os.system('afplay ./tmp/sound.mp3')  # Works only on Mac OS, sorry
    os.remove('./tmp/sound.mp3')


def classify_deployed(file_name):
    payload = None
    with open(file_name, 'rb') as f:
        payload = f.read()
        payload = bytearray(payload)

    return payload

# Coffee,Coffee Cup,Raspberry Pie,Timmy,Water Bottle
labels = ['Coffee', 'Coffee Cup', 'Marker', 'Raspberry Pie', 'Timmy','Water Bottle']
voice = {
    labels[0]: "This is a {} mug with a probability of {}.  It is not recyclable ",
    labels[1]: "This is a {} with a probability of {}. Please recycle this item.  ",
    labels[2]: "This is a {} with a probability of {}.  While colorful and fun you cannot recycle them.  Dont smell them, you will leave a mark on your nose.",
    labels[3]: "This is a {} with a probability of {}.  You can run SageMaker Neo on this super cool device,  but but you cannot recycle this.",
    labels[4]: "This is {} the geek monkey with a probability of {}.  He can help you answer any questions, however you cannot recycle him.  That would not be right.",
    labels[5]: "This is a {} with a probability of {}.  While you cannot recycle it, good for your for using a reusable container.",
}

def play_audio(predicted_label, predicted_probability):
    prob_str = f"{int(predicted_probability*100)} percent"

    print(f"Play: {predicted_label}, {predicted_probability}")
    audio_string = voice[predicted_label]
    audio_string = audio_string.format(predicted_label, prob_str)
    audio_string += " Thanks for using Recycle Goo Roo"

    speak(connectToPolly(), audio_string)

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
    predicted_probability = response_json['body']['predicted_probability']
    print(f"Status Code: {response_json['statusCode']}")
    print(f"Predicted Label: {response_json['body']['predicted_label']}")
    print(f"Predicted Probability: {predicted_probability}")
    print("")
    print(f"All Predictions: {response_json['body']['predictions']}")
    print("-------------------")

    if status_code == 200:
        if predicted_probability > 0.40:
            play_audio(predicted_label, predicted_probability)
        else:
            prob_str = f"{int(predicted_probability * 100)} percent"
            speak(connectToPolly(), f"I think this is a {predicted_label} but the probability is very low at {prob_str}.  I cannot tell if you should recycle this item or not.")
    else:
        speak(connectToPolly(), f"DOH, something went wrong, can you try again later")

