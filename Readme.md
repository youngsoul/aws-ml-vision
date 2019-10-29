# This repo will hold the vision project for the AWS ML Course

## EOD Info

### Github
https://github.com/youngsoul/aws-ml-vision

### Goal

Dynamically capture and train an image-classification model to detect recycleable objects.

### S3

vision-recycle

Since the data will be captured as we go, we dont have data as of now.

## Background

Take images from the computer web cam as the training set of data.  

This data will be saved in an S3 bucket, and used to train the image-classification model.  

New images will be taken from the web cam for object detection to predict what object it is, and whether it is recycleable


## Tasks

### Mitch

[] review youtube video on image-classification

[] create the initial jupyter notebook for image classification

[] assume that a dataset will be available in the S3 bucket

[] assume the image size is 224x224

[] ultimately provide a sagemaker endpoint

### Pat
[] create github repo

[] write program to capture images from web cam

[] write program to resize images to 224x224

[] write program to capture new image and call sagemaker endpoint


