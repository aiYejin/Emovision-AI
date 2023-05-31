import cv2
import mediapipe as mp
import numpy as np
import utils
import os

# 얼굴 인식 모델 호출
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5, model_selection=1)
# 데이터 경로
directory='./data'

for root, dirs, files in os.walk(directory):
    # 폴더에 있는 모든 파일 순회
    for file in files:
        file_path = os.path.join(root, file)
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            # 이미지 파일인 경우 작업 수행
            try:
                image = cv2.imread(file_path)
                if image is not None:
                    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.7) as face_detection:
                        image.flags.writeable = False
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        results = face_detection.process(image)

                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                        if results.detections:
                            # 검출된 얼굴들에 한해 작업 진행
                            for detection in results.detections:
                                # 키포인트로 affine 변환
                                keypoints = detection.location_data.relative_keypoints
                                keypoints = np.array([(keypoint.x, keypoint.y) for keypoint in keypoints], dtype=np.float32)
                                
                                src_points = np.array([keypoints[0], keypoints[1], keypoints[2], keypoints[3]])
                                dst_points = np.array([(33,33), (97, 33), (65, 65), (65, 97)])

                                w, h = image.shape[1], image.shape[0]
                                src_points[:, 0] *= w
                                src_points[:, 1] *= h
                                M, _ = cv2.estimateAffine2D(src_points, dst_points)

                                # 정렬된 얼굴 부분 크롭
                                face_aligned = cv2.warpAffine(image, M, (0,0))
                                face_result = face_aligned[0:128, 0:128]

                                file_name = os.path.splitext(file)[0]
                                # 원래의 파일에 덮어씌움
                                new_file_path = os.path.join(root, file_name + ".jpg")
                                cv2.imwrite(new_file_path, face_result)
                # 예외 처리
                else:
                    print("Failed to read image:", file_path)
            except Exception as e:
                print("Error processing image:", file_path)
                print("Error:", str(e))
리