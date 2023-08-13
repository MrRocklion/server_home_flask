from flask import Flask,render_template,Response,request,jsonify
import cv2
from waitress import serve
from flask_cors import CORS
import socket

app=Flask(__name__)
CORS(app)
camera=cv2.VideoCapture(0)

def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')




@app.route('/angulo', methods=['POST'])
def test():
    input_json = request.get_json(force=True) 
    # force=True, above, is necessary if another developer 
    # forgot to set the MIME type to 'application/json'
    print('data from client:', input_json)
    enviarDato(input_json['angulo'])
    dictToReturn = {'answer':42}
    return jsonify(dictToReturn)

def enviarDato(angulo):
    s = socket.socket()
    print(angulo)
    if(angulo <255):
        s.connect(('192.168.1.5',8090)) 
        s.send(angulo.to_bytes(1, 'big'))
        s.close()
        print("me desconecto")
    else:
        print("angulo muy alto")

mode = "dev"
if __name__ == '__main__':
    if mode == "dev":
        app.run(host='0.0.0.0', port=50100, debug=True)
    else:
        serve(app, host='0.0.0.0', port=50100, threads=4)