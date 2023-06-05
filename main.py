import cv2
import os
import mediapipe as mp
from keras.models import load_model
import numpy as np
import utils
import serial

ser=serial.Serial("COM3", 9600) # 아두이노 포트 연결

# 진동 패턴 전송 함수
def send_vibration_pattern(pattern):
    ser.write(pattern.encode())
# 얼굴 인식 결과, 진동 패턴 전송
def face_signal(face_identity):
    if face_identity == "jin":
        send_vibration_pattern("J")
    elif face_identity == "eun":
        send_vibration_pattern("E")

# 표정 인식 결과와 진동 패턴 전송
def expression_signal(expression):
    if expression == "neutral":
        send_vibration_pattern("N")
    elif expression == "smile":
        send_vibration_pattern("H")
    elif expression == "sad":
        send_vibration_pattern("S")
    elif expression == "frown":
        send_vibration_pattern("F")
    elif expression == "surprised":
        send_vibration_pattern("U")

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# 얼굴 인식, 표정 인식 파일 불러오기
Face_recognition_model_path = 'best_face_model.h5'
Emotion_recognition_model_path = 'best_emotion_model.h5'
recognition_model = load_model(Face_recognition_model_path)
emotion_model = load_model(Emotion_recognition_model_path)

# 이름과 표정의 라벨 설정
names=['min','gyu','eun','others','gun','jin']
emotions=['frown','smile','neutral','sad','surprised']

# mediapipe의 Facedetection 불러오기
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5, model_selection=1)
jin = 0
eun = 0
# 웹캠 열기
cap = cv2.VideoCapture(1)
frame_number=0
fps = cap.get(cv2.CAP_PROP_FPS)
# 얼굴 인식
with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
    # 카메라가 열려있는 동안에
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
      # 카메라가 열려있지 않으면, 종료
            break

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # 얼굴이 감지되면
        if results.detections:
            # 감지된 얼굴들 순회
            for detection in results.detections:
                # 얼굴 키포인트 저장
                keypoints = detection.location_data.relative_keypoints
                keypoints = np.array([(keypoint.x, keypoint.y) for keypoint in keypoints], dtype=np.float32)
                
                # 키포인트를 이용하여 얼굴 정렬
                face_result = utils.align(image, keypoints)

                # 정렬된 얼굴을 모델의 입력에 맞게 흑백으로 바꾸고 resize
                face_result = cv2.cvtColor(face_result, cv2.COLOR_BGR2GRAY)
                face_result = face_result.reshape((1, 128, 128, 1))
                # face recognition
                text, color=utils.predict(recognition_model, face_result, names)
                # 표정 인식
                emotion, e_color=utils.emotion(emotion_model, face_result, emotions)



                if text=="eun":
                    eun+=1
                elif text=="jin":
                    jin+=1
                
                # 처음 얼굴 인식이 되었을 때에만 진동을 보냄
                if text=="eun" and eun ==1:
                    face_signal(text)
                elif text=="jin" and jin==1:
                    face_signal(text)
                    

                frame_number+=1

                if(frame_number%10==0): # 10번에 한 번만 진동을 보냄
                    expression_signal(emotion)

                # 얼굴 영역에 사각형 및 이름, 표정 출력
                bbox = detection.location_data.relative_bounding_box
                x, y, w, h = int(bbox.xmin * image.shape[1]), int(bbox.ymin * image.shape[0]), int(bbox.width * image.shape[1]), int(bbox.height * image.shape[0])
          
                cv2.rectangle(image, (x, y), (x+w, y+h), color, thickness=2)
                cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=color, thickness=2)
                cv2.putText(image, emotion, (x, y+h+15), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=e_color, thickness=1)

        cv2.imshow('frame', image)

        # 'q'를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break


ser.close()
cap.release()
cv2.destroyAllWindows()
