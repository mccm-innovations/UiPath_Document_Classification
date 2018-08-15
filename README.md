# UiPath Document Classification
## Inspiration
The line between RPA and Artificial Intelligence is getting closer. We provide a document classifier developed with Deep Neural Networks which can be deployed in a server and used from a RPA project through an API.

Currently, our model is able to categorize 5 types of documents: invoices, passports, driving licences, Spanish ID cards, and Spanish ID cards 3.0.

For example, this project may be used to classify email attachments and forward them to different business areas depending on its category.

## What it does
Given a PDF or image file, UiPath make an API call to the inference server in order to classify the input file in one of the following categories: invoices, passports, driving licences, Spanish ID cards, and Spanish ID cards 3.0.

## How we built it
We built this in UiPath using the HTTP Request Activity which makes a call to the inference server.  

The inference server is built with flask and gunicorn. It exposes an API endpoint that executes the document classification model trained with Keras and returns its result in JSON format.

More details about the inference server can be found in [Configuring an inference server](https://github.com/mccm-innovations/UiPath_Document_Classification/tree/master/inference_server).

## Video demo
[![UiPath Document Classification Video Demo](https://img.youtube.com/vi/T_pHknyUcIk/0.jpg)](https://www.youtube.com/watch?v=T_pHknyUcIk "UiPath Document Classification Video Demo")
