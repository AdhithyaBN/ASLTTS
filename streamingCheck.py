import io
import cv2
import time
import numpy as np
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/stream")
async def stream_video():
    # Start capturing video from the client's camera
    capture = cv2.VideoCapture(0)

    # Set the video capture parameters
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        # Read a video frame from the camera
        ret, frame = capture.read()

        if not ret:
            # End of video stream
            break

        # Encode the video frame as JPEG
        ret, jpeg = cv2.imencode(".jpg", frame)

        # Yield the JPEG-encoded frame to the client
        yield jpeg.tobytes()

        # Add a delay to simulate streaming
        time.sleep(0.1)

    # Release the video capture device
    capture.release()

@app.get("/streaming")
async def streaming_video():
    # Start capturing video from the client's camera
    capture = cv2.VideoCapture(0)

    # Set the video capture parameters
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        # Read a video frame from the camera
        ret, frame = capture.read()

        if not ret:
            # End of video stream
            break

        # Encode the video frame as JPEG
        ret, jpeg = cv2.imencode(".jpg", frame)

        # Return a streaming response with the JPEG-encoded frame
        yield StreamingResponse(io.BytesIO(jpeg.tobytes()), media_type="image/jpeg")

        # Add a delay to simulate streaming
        time.sleep(0.1)

    # Release the video capture device
    capture.release()
