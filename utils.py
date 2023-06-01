import numpy as np
import cv2

# 얼굴 정렬
def align(image, keypoints):
    # 받아온 키포인트를 배열에 저장
    src_points = np.array([keypoints[0], keypoints[1], keypoints[2], keypoints[3]])
    # 정렬 후 키포인트의 위치
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
    return face_result

# face recognition
def predict(model, face_result, names):
    predicted_probs = model.predict(face_result)[0]
    predicted_class = np.argmax(predicted_probs)
    if predicted_probs[predicted_class] > 0.8 and (names[predicted_class]=='jin' or names[predicted_class]=='eun'):
        text = names[predicted_class]
        color = (0, 255, 0)
    # 얼굴 인식 결과가 학습한 인물이 아닌 경우
    else:
        text = 'Unknown'
        color = (0, 0, 255)
    return text, color

# 표정 인식
def emotion(model, face_result, emotions):
    predict_emotion = model.predict(face_result)[0]
    predicted_class = np.argmax(predict_emotion)
    print(predict_emotion[predicted_class])
    if predict_emotion[predicted_class] > 0.8:
        text = emotions[predicted_class]
        color = (0, 0, 255)
    else:
        text = 'neutral'
        color = (0, 0, 255)
    return text, color

# 모델 로드
def load_model(filepath):
    model = load_model(filepath)
    return model