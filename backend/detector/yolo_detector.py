# backend/detector/yolo_detector.py

from ultralytics import YOLO
import cv2
import os

# 모델 로드 (YOLOv8 탐지용)
model_path = os.path.join('model', 'best.pt')
model = YOLO(model_path)

def detect_tanks(video_path, save_path=None):
    """
    YOLOv8로 입력 영상에서 전차 탐지
    - video_path: 분석할 영상 경로
    - save_path: 탐지 결과 저장 경로 (선택)
    - return: 탐지된 프레임 정보 리스트 (예: [{'frame': 32, 'label': 'T-90', 'confidence': 0.91, 'bbox': [x1, y1, x2, y2]}, ...])
    """
    cap = cv2.VideoCapture(video_path)
    detections = []
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id]
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append({
                    'frame': frame_idx,
                    'label': label,
                    'confidence': conf,
                    'bbox': [x1, y1, x2, y2]
                })

                # 박스 그리기 (선택)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, f"{label} ({conf:.1%})", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # 결과 저장 (선택)
        if save_path:
            os.makedirs(save_path, exist_ok=True)
            out_file = os.path.join(save_path, f'frame_{frame_idx}.jpg')
            cv2.imwrite(out_file, frame)

        frame_idx += 1

    cap.release()
    return detections
