import cv2
import mediapipe as mp
import numpy as np
import utils

# 얼굴 인식 모델 호출
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5, model_selection=1)

# 웹캠 호출
cap = cv2.VideoCapture(0)
frame_number=0
image_num=0

with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
      # 웹캠이 안 열려있으면 break
            break

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.detections:
            for detection in results.detections:
                # 키포인트를 이용하여 얼굴을 정렬
                keypoints = detection.location_data.relative_keypoints
                keypoints = np.array([(keypoint.x, keypoint.y) for keypoint in keypoints], dtype=np.float32)

                face_result = utils.align(image, keypoints)

                frame_number+=1
                if frame_number % 30 == 0: # 30 프레임 당 한 번
                    image_num+=1
                    # 순서대로 숫자를 붙여 이름으로 저장
                    filename=f"{image_num}.jpg"
                    cv2.imwrite(filename, face_result)
                    # 저장한 이미지 보여줌
                    cv2.imshow('face_aligned', face_result)

        # q를 누르거나, 1000장을 찍으면 종료
        if cv2.waitKey(1) & 0xFF == ord('q') or image_num==1000: # 1000장 찍으면 종료
                break

cap.release()
cv2.destroyAllWindows()
