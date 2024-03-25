from io import BytesIO
from flask import Flask, request, send_file
import cv2
import numpy as np

app = Flask(__name__)

a = [5,]

@app.route('/receive_frame', methods=['POST'])
def receive_frame():
    frame = request.files['frame'].read()
    nparr = np.frombuffer(frame, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Get thermal value from request
    thermal = float(request.form['thermal'])

    # Process your image with the received thermal value
    a.clear()
    a.append(thermal)

    cv2.imwrite('result.jpg', img)

    return 'Frame received and processed successfully!'

@app.route('/send_frame', methods=['POST'])
def send_frame():
    # Read the image file using OpenCV
    image = cv2.imread("result.jpg")

    # Convert the image to JPEG format
    _, buffer = cv2.imencode('.jpg', image)

    # Return the image
    return send_file(BytesIO(buffer), mimetype='image/jpeg')

@app.route('/send_thermal', methods=['POST'])
def send_thermal():
    print(a[0])
    return str(a[0])

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
