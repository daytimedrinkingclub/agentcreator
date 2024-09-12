# Flask Calculator

This is a simple calculator web application built using Flask. It provides basic arithmetic operations such as addition, subtraction, multiplication, and division.

## Features

- Simple and intuitive user interface
- Supports addition, subtraction, multiplication, and division
- Error handling for invalid inputs and division by zero

## Requirements

- Python 3.7+
- Flask

## Installation

1. Clone this repository
2. Install the required packages using `pip install -r requirements.txt`
3. Run the application using `python app.py`

## Usage

1. Open your web browser and go to `http://localhost:5000`
2. Enter two numbers and select an operation
3. Click the "Calculate" button to see the result

## Docker

This application can also be run using Docker. To build and run the Docker container, use the following commands:

```
docker build -t flask-calculator .
docker run -p 5000:5000 flask-calculator
```

Then access the application at `http://localhost:5000` in your web browser.