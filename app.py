from flask import Flask, render_template, Response, request
import cv2
import os

app = Flask(__name__)

# Initialize webcam
camera_index = 0  # Default camera index
camera = cv2.VideoCapture(camera_index)

# Create folders for defects
folders = ['data/holes', 'data/foreign_yarn', 'data/surface_contamination', 'data/slubs']
for folder in folders:
    os.makedirs(folder, exist_ok=True)

def generate_frames():
    while True:
        # Capture frame from webcam
        success, frame = camera.read()
        if not success:
            print("Failed to grab frame from camera")
            break
        else:
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("Failed to encode frame")
                continue
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture_image():
    """Capture and save an image."""
    defect_type = request.form.get('defect_type')
    success, frame = camera.read()
    if success and defect_type:
        folder_path = f'data/{defect_type}'
        file_name = f"{folder_path}/{defect_type}_{len(os.listdir(folder_path)) + 1}.jpg"
        cv2.imwrite(file_name, frame)
        print(f"Image saved to {file_name}")
    else:
        print("Failed to capture image")
    return '', 204

@app.route('/control', methods=['POST'])
def control_camera():
    """Start, pause, or stop the camera."""
    action = request.form.get('action')
    global camera
    if action == "stop":
        camera.release()
        print("Camera stopped")
    elif action == "start":
        if not camera.isOpened():
            camera = cv2.VideoCapture(camera_index)
            print("Camera started")
    return '', 204

if __name__ == '__main__':
    # Check if the camera is accessible
    if not camera.isOpened():
        print(f"Failed to open camera at index {camera_index}. Check the index or permissions.")
        exit(1)
    
    app.run(debug=True)
