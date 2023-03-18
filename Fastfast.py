from fastapi import FastAPI,Request,Response
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from utilityALSTTS import open, check_prediction,play_text
import cv2
from fastapi import Request
import base64
import time
templates = Jinja2Templates(directory="templates/")


application = FastAPI()

origins = ["*"]

application.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@application.get("/stream")
async def read_root(request:Response):
    open()
    cv2.destroyAllWindows()

def gen_frames():
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()

        if not success:
            break

        # Convert the frame to JPEG format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        yield jpg_as_text

    cap.release()

@application.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# @application.get("/video_feed")
# async def video_feed():
#     return Response(gen_frames(),
#                     media_type='multipart/x-mixed-replace; boundary=frame')



@application.get("/base")                                   #Returns the status of the server
async def root():
    return {"message": "Server Active"}

@application.get("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

camera = cv2.VideoCapture(0)

@application.get("/gen_frames")    
def gen_frames():  
    prev_frame_time = 0
  
# used to record the time at which we processed current frame
    new_frame_time = 0
  
    while True:
        success, image = camera.read()
        if not success:
            break
        else:
            font = cv2.FONT_HERSHEY_SIMPLEX
            # time when we finish processing for this frame
            new_frame_time = time.time()
        
            # Calculating the fps
        
            # fps will be number of frame processed in given time frame
            # since their will be most of time error of 0.001 second
            # we will be subtracting it to get more accurate result
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time
        
            # converting the fps into integer
            fps = int(fps)
        
            # converting the fps to string so that we can display it on frame
            # by using putText function
            fps = str(fps)
        
            # putting the FPS count on the frame
            cv2.putText(image, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)


            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            #add your asl code over here

            ret, buffer = cv2.imencode('.jpg', image)
            image = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')





    









