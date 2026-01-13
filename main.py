import cv2
import os
import argparse
import mediapipe as mp

#function to detect faces
def process_img(img, face_detection):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    out = face_detection.process(img_rgb)
    H, W, _ = img.shape

    #if no human face found in image
    if out.detections is not None:
        for detection in out.detections:
            location_data = detection.location_data
            bbox = location_data.relative_bounding_box

            x1, y1, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height

            x1 = int(x1 * W)
            y1 = int(y1 * H)
            w = int(w * W)
            h = int(h * H)

            # img = cv2.rectangle(img, (x1, y1), (x1+w, y1+h), (0,255,0), 5)
#blur faces
            img[y1:y1+h, x1:x1+w, :] = cv2.blur(img[y1:y1+h, x1:x1+w, :], (30, 30))

    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    return img

#This hard-codes the arguments for each mode (webcam, video, image)
#Code uses a more flexible version instead

# args = argparse.ArgumentParser()
# args.add_argument("--mode", default='webcam') #depending on video, image or webcam
# args.add_argument("--filePath", default=None) #'./video/test.mp4'
# args = args.parse_args()

mode_input = input("Enter type of mode: ") #image, video, webcam

#detect faces in image
mp_face_detection = mp.solutions.face_detection
with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    if mode_input == 'image':
        #read image
        in_path = os.path.join('.', 'image', 'face.jpg')
        out_path = os.path.join('.', 'image', 'out.jpg')
        
        img = cv2.imread(in_path)

        img = process_img(img, face_detection)

        #saving image
        cv2.imwrite(out_path, img)

    elif mode_input == 'video':
        in_path = os.path.join('.', 'video', 'test.mp4')
        out_path = os.path.join('.', 'video', 'out.mp4')
        
        cap = cv2.VideoCapture(in_path)
        ret, frame = cap.read()

        output = cv2.VideoWriter(out_path,
                                 cv2.VideoWriter_fourcc(*'MP4V'),
                                 30, #can be changed by taking the frame from the original video
                                 (frame.shape[1], frame.shape[0]))
        while ret:
            img = process_img(frame, face_detection)
            output.write(frame)
            ret, frame = cap.read()

        cap.release()
        output.release()

    elif mode_input == 'webcam':
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()

        while ret:
            frame = process_img(frame, face_detection)
            cv2.imshow('frame', frame)

            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

            ret, frame = cap.read()
        
        cap.release()

    else:
        print("Invalid Mode..")