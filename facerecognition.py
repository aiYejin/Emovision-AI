import cv2
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
import mediapipe as mp
from keras.models import load_model
import numpy as np

# 모델 불러오기
model_path = 'my_model.h5'
model = load_model(model_path)
names=['gun','kyu','yejin']

# Initialize face detector
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5, model_selection=1)

# Initialize the webcam
cap = cv2.VideoCapture(0)

with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'
            break
	# 성능을 향상시키려면 이미지를 작성 여부를 False으로 설정하세요.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.detections:
            # Extract the relative keypoints of the face
            for detection in results.detections:
                keypoints = detection.location_data.relative_keypoints
                keypoints = np.array([(keypoint.x, keypoint.y) for keypoint in keypoints], dtype=np.float32)
                
                # Compute the transformation matrix using the keypoints
                src_points = np.array([keypoints[0], keypoints[1], keypoints[2], keypoints[3]])
                dst_points = np.array([(0.45,0.45), (0.55, 0.45), (0.5, 0.5), (0.5, 0.55)])
                w, h = image.shape[1], image.shape[0]
                src_points[:, 0] *= w
                src_points[:, 1] *= h
                dst_points[:, 0] *= w
                dst_points[:, 1] *= h
                M, _ = cv2.estimateAffine2D(src_points, dst_points)

                # Apply the transformation to the face region
                face_aligned = cv2.warpAffine(image, M, (0,0))
                face_result = face_aligned[175:303, 255:383]

                face_result = cv2.cvtColor(face_result, cv2.COLOR_BGR2GRAY)
                face_result = face_result.reshape((1, 128, 128, 1))
                predicted_probs = model.predict(face_result)[0]
                predicted_class = np.argmax(predicted_probs)

                if predicted_probs[predicted_class] > 0.5:
                    predicted_name = predicted_class
                    text = names[predicted_name]
                    color = (0, 255, 0)
                # 얼굴 인식 결과가 학습한 인물이 아닌 경우
                else:
                    text = 'Unknown'
                    color = (0, 0, 255)
                # 얼굴 영역에 사각형 및 이름 출력
                bbox = detection.location_data.relative_bounding_box
                x, y, w, h = int(bbox.xmin * image.shape[1]), int(bbox.ymin * image.shape[0]), int(bbox.width * image.shape[1]), int(bbox.height * image.shape[0])
          
                cv2.rectangle(image, (x, y), (x+w, y+h), color, thickness=2)
                cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=color, thickness=2)

    # 프레

            # Show the original frame
        cv2.imshow('frame', image)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
