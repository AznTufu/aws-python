# AWS Python Project

This is a student project to learn how to interact with AWS API and Lambdas using Python.

## Project Overview

This project creates a Python script that interacts with two AWS API endpoints:

1. `/manageUser`: Used to retrieve user information
2. `/getToken`: Used to obtain an API key for authentication

We have used multithreading to process multiple requests simultanously.

## Prerequisites

Before running this project, ensure you have:

- Python installed on your system (We have used python 3.11 on this project, consider installing this version or adapt the repo to your personal version)

## How to Run the Project

1. Clone this repository to your local machine
2. Install required dependencies:
   pip install requests

3. Open a terminal and navigate to the project directory
4. Run the script using Python:
   python test.py

## API Endpoints

The project interacts with two AWS API Gateway endpoints:

### `/manageUser`

This endpoint retrieves information about users. It requires authentication via an API key.

- **Method**: GET
- **Endpoint URL**: https://pdfv2l2ceg.execute-api.eu-west-1.amazonaws.com/dev/manageUser
- **Authentication**: Uses an API key sent in the request header

### `/getToken`

This endpoint generates a token for authentication. It returns a hash value that can be used to authenticate subsequent requests.

- **Method**: POST
- **Endpoint URL**: https://pdfv2l2ceg.execute-api.eu-west-1.amazonaws.com/dev/getToken
- **Request Body**: JSON object with an email field
- **Response**: Returns a hash value for authentication

If you have any question about this you can contact us at these emails:

Tony ZHANG: tony.zhang@edu.devinci.fr
Romain PARISOT: romainparisot.pro@gmail.com
