import cv2
import mediapipe as mp
import numpy as np

# Initialize face detector
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5, model_selection=1)

# Initialize the webcam
cap = cv2.VideoCapture(0)
frame_number=0
image_num=0

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
                dst_points = np.array([(0.4,0.4), (0.6, 0.4), (0.5, 0.5), (0.5, 0.6)])
                w, h = image.shape[1], image.shape[0]
                src_points[:, 0] *= w
                src_points[:, 1] *= h
                dst_points[:, 0] *= w
                dst_points[:, 1] *= h
                M, _ = cv2.estimateAffine2D(src_points, dst_points)

                # Apply the transformation to the face region
                face_aligned = cv2.warpAffine(image, M, (0,0))
                face_result = face_aligned[111:367, 191:447]

                frame_number+=1
                if frame_number % 30 == 0: # 30 프레임 당 한 번
                    image_num+=1
                    filename=f"{image_num}.jpg"
                    cv2.imwrite(filename, face_result)

                    cv2.imshow('face_aligned', fac료e_result)

        cv2.imshow('frame', image)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q') or image_num==100: # 100장 찍으면 종료
                break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
