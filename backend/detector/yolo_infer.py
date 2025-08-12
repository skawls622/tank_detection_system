import os
import cv2
from ultralytics import YOLO



# YOLO 모델 로딩 (한번만)
MODEL_PATH = r"D:\Final_Project\best.pt"
model = YOLO(MODEL_PATH)

def detect_video(input_path):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError("영상 열기 실패!")


    frame_results = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(source=frame, conf=0.3, save=False, verbose=False)

        annotated_frame = results[0].plot()  # 바운딩박스 그려진 프레임
        frame_results.append(annotated_frame)

    cap.release()
    return frame_results