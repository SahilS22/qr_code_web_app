from flask import Flask, render_template, request, send_file
import qrcode
from PIL import Image
import os
import re
from pyzbar.pyzbar import decode
import csv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

@app.route('/')
def index():
    return render_template('index.html')

def sanitize_filename(data):
    """Sanitize the filename by removing invalid characters."""
    return re.sub(r'[<>:"/\\|?*;]', '_', data)

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    qr_type = request.form['qr_type']
    fill_color = request.form['fill_color']
    back_color = request.form['back_color']

    # Determine the data to encode
    if qr_type == 'text':
        data = request.form['data']
        if not data:  # Check for empty data
            return "Error: Data for QR code cannot be empty.", 400
        print(f"Generating QR for text: {data}")  # Debug info
    elif qr_type == 'wifi':
        ssid = request.form['ssid']
        password = request.form['password']
        encryption = request.form['encryption']
        hidden = request.form['hidden']
        data = f"WIFI:S:{ssid};T:{encryption};P:{password};H:{hidden};;"
        print(f"Generating QR for Wi-Fi: {data}")  # Debug info

    # Sanitize the filename
    safe_data = sanitize_filename(data)
    qr_path = os.path.join(app.config['UPLOAD_FOLDER'], f'qr_{safe_data}.png')

    try:
        # Generate QR code
        img = qrcode.make(data)
        img = img.convert("RGB")

        # Fill colors based on the provided color options
        fill_rgb = tuple(int(fill_color[i:i + 2], 16) for i in (1, 3, 5))
        back_rgb = tuple(int(back_color[i:i + 2], 16) for i in (1, 3, 5))

        for x in range(img.size[0]):
            for y in range(img.size[1]):
                current_color = img.getpixel((x, y))
                if current_color == (255, 255, 255):  # white background
                    img.putpixel((x, y), back_rgb)
                else:  # black foreground
                    img.putpixel((x, y), fill_rgb)

        # Save the QR code
        img.save(qr_path)
        print(f"QR code saved to: {qr_path}")  # Debug info

        return send_file(qr_path)
    except Exception as e:
        print(f"Error generating QR code: {str(e)}")
        return "Error generating QR code.", 500

@app.route('/batch_generate', methods=['POST'])
def batch_generate():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Save the uploaded CSV file temporarily
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.csv')
    file.save(temp_path)

    try:
        # Read the CSV and generate QR codes for each line
        with open(temp_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # Assuming the QR code data is in the first column of the CSV
                qr_data = row[0] if row else ""
                if qr_data:
                    # Generate QR code for this data (you could call a function here)
                    print(f"Generating QR for: {qr_data}")  # Replace this with actual generation logic
                else:
                    print("Empty row, skipping...")

        return "Batch QR Code generation completed.", 200

    except Exception as e:
        print(f"Error in batch generation: {str(e)}")
        return "Error processing the batch generation.", 500

@app.route('/decode_qr', methods=['POST'])
def decode_qr():
    # Implement QR code decoding logic
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    # Save the uploaded image temporarily
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_qr.png')
    file.save(temp_path)

    # Decode the QR code
    decoded_objects = decode(Image.open(temp_path))
    decoded_text = [obj.data.decode('utf-8') for obj in decoded_objects]

    # Remove the temporary file
    os.remove(temp_path)

    return {"decoded_data": decoded_text}

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
