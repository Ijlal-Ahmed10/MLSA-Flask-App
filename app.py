from flask import Flask, Response
import cv2

app = Flask(__name__)

def generate_frames():
    
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError("Error: Cannot open video source.")
    
    while True:
        try:
            success, frame = camera.read()
            if not success:
                print("Error: Cannot read from camera.")
                break
            
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("Error: Failed to encode frame.")
                break

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        except cv2.error as e:
            print(f"OpenCV Error: {e}")
            break

    camera.release()


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

mode = 'dev'

if __name__ == '__main__':
    if mode == 'dev':
        app.run(host='0.0.0.0', port=5000, debug=True)  # stream on http://<laptop-ip>:5000/video_feed

    else:
        app(host='0.0.0.0', port=5000, debug=False)
