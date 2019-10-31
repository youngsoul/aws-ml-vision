# This repo will hold the vision project for the AWS ML Course

## Project Dependencies

Python 3.6+

OpenCV 4.0.1+

requests
boto3

### Github
https://github.com/youngsoul/aws-ml-vision

### Goal

Dynamically capture and train an image-classification model to detect recycleable objects.

## Background

Take images from the computer web cam as the training set of data.  

This data will be saved in an S3 bucket, and used to train the image-classification model.  

New images will be taken from the web cam for object detection to predict what object it is, and whether it is recycleable


## Lambda

Access via API Gateway POSt that will send the image data in the payload body as a b64 encoded byte array.

The Lambda will call a SageMaker endpoint with the image.  The SageMaker model will perform an image classification based on the 6 images return an array of probabilities.

The Lambda will determine which label was the most likely and format a response.

There are 2 environment variables for the Lambda.

#### ENDPOINT_NAME

The name of the SageMaker Endpoint

#### LABELS

An ordered list of Friendly names that should match the order of the labels used to train.


### Code
predict_image_lambda.py


## API Gateway

Create an API Gateway POST that will connect to the Lambda

## Rest Client

### Code
predict_image_rest_client.py

This client will take the image, and create a b64 encoded byte array and make an HTTP POST request to the API Gateway.  

When the client receives the response, it will then format a message based on the predicted image and use the AWS Polly service to create an MP3 to play.

## SageMaker Notebook

Recycle Guru - Sagemaker Image Classifer via Transfer Learning.ipynb

This notebook will train the model and create a model endpoint.  The notebook will create a named SageMaker model endpoint and that name must be used in the Lambda.


## Presentation Notebook

RecycleGuru.ipynb

This notebook is the presentation and client notebook

