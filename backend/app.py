import os
from flask import Flask, render_template, request, redirect, url_for, flash
from ultralytics import YOLO
from utils import get_tank_info_from_csv

app = Flask(__name__)
app.secret_key = 'supersecret'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        flash('파일이 없습니다!')
        return redirect(url_for('index'))

    file = request.files['video']
    if file.filename == '':
        flash('파일이 선택되지 않았습니다!')
        return redirect(url_for('index'))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # YOLO 추론 실행
    model = YOLO("D:/Final_Project/service_flask/best.pt")  # 모델 경로는 맞게 수정
    results = model.predict(source=filepath, save=False)  # 결과 저장은 일단 생략

    # 첫 번째 탐지 결과에서 클래스명 추출
    if results and results[0].boxes and results[0].boxes.cls.numel() > 0:
        class_id = int(results[0].boxes.cls[0])
        class_name = model.names[class_id]
    else:
        flash("탐지 결과가 없습니다.")
        return redirect(url_for('index'))

    # 전차 제원 CSV에서 정보 추출
    tank_info = get_tank_info_from_csv(class_name)

    if not tank_info:
        flash(f"'{class_name}'에 해당하는 전차 정보가 없습니다.")
        return redirect(url_for('index'))

    # 추론 → 결과 페이지로 직접 렌더링
    return render_template('tank_info.html', tank=tank_info)


@app.route('/result/<tank_name>')
def show_tank_info(tank_name):
    tank_info = get_tank_info_from_csv(tank_name)

    if not tank_info:
        flash(f"'{tank_name}'에 해당하는 전차 정보가 없습니다.")
        return redirect(url_for('index'))

    return render_template('tank_info.html', tank=tank_info)


if __name__ == '__main__':
    app.run(debug=True)