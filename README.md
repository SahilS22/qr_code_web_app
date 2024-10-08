# QR Code Generator

A simple and user-friendly QR Code Generator web application built with Flask. This application allows users to create QR codes for different types of data, including plain text and Wi-Fi credentials. Users can also customize QR code colors and upload logos.

## Features

- **QR Code Types**: Generate QR codes for text and Wi-Fi credentials.
- **Color Customization**: Choose foreground and background colors for your QR codes.
- **Logo Upload**: Upload a logo to be embedded within the QR code (optional).
- **Batch QR Code Generation**: Generate multiple QR codes from a CSV file (feature not yet implemented).
- **QR Code Decoding**: Upload a QR code image to decode and retrieve the embedded data.

## Tech Stack

- **Backend**: Flask
- **QR Code Generation**: [qrcode](https://pypi.org/project/qrcode/) Python library
- **QR Code Decoding**: [pyzbar](https://pypi.org/project/pyzbar/) Python library
- **Frontend**: HTML, CSS, JavaScript

## Installation

### Prerequisites

Make sure you have Python 3.x installed on your system. You also need to install the required packages.

Usage
Generate QR Codes:

Select the type of QR code (Text or Wi-Fi).
Enter the relevant data.
Customize the QR code color if desired.
Click on "Generate QR Code" to create the QR code.
Batch QR Code Generation:

Upload a CSV file (not yet implemented).
Decode QR Codes:

Upload an image of the QR code to retrieve the encoded data.

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/qr-code-generator.git
   cd qr-code-generator
