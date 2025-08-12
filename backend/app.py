import os
from datetime import timedelta

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
    send_from_directory,
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# ----- 모델/DB 연동 (프로젝트에 맞게 이미 존재한다고 가정) -----
from detector.yolo_detector import detect_and_return_summary
from db.mysql_connector import get_connection

# =========================
# 경로 설정
# =========================
# service_flask/
#   backend/               ← 이 파일(app.py)
#     static/
#       app/               ← React 빌드 산출물(dist 복사 위치)
#     templates/           ← Jinja 템플릿(landing, login 등)
#   frontend/
#     static/              ← (프로젝트 기존 정적자원)
#     templates/           ← (프로젝트 기존 템플릿, 필요 시 사용)
#   frontend-react/        ← React 소스(개발 전용)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, "frontend", "templates")           # Jinja 템플릿
STATIC_DIR = os.path.join(BASE_DIR, "frontend", "static")        # 기존 정적(유지)
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")                   # 업로드
APP_DIST = os.path.join(BACKEND_DIR, "static", "app")            # React 빌드 결과

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Flask 앱 생성
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = os.getenv("SECRET_KEY", "change_me_in_env")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)
app.config["UPLOAD_FOLDER"] = UPLOAD_DIR

# =========================
# CORS (개발모드용: Vite 5173)
# =========================
# prod(통합 배포)에서는 /app 으로 동일 포트라 CORS 불필요. 남겨둬도 무해.
try:
    from flask_cors import CORS

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": ["http://localhost:5173", "http://127.0.0.1:5173"]
            }
        },
    )
except ImportError:
    print("[경고] flask-cors 미설치. 개발 중 React(5173)에서 호출 시 CORS 에러 가능 → pip install flask-cors")

# =========================
# SSR 라우트 (Jinja)
# =========================
@app.route("/")
def index():
    # 랜딩 페이지
    return redirect(url_for("serve_app"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        usercode = request.form.get("userid", "").strip()
        raw_password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        username = request.form.get("name", "").strip()
        affiliation_id = request.form.get("unit", "").strip()     # DB 컬럼: Afflication_ID (DB와 철자 통일)
        tank_id = request.form.get("tank", "").strip()
        field = request.form.get("rank", "").strip()

        if not usercode or not raw_password or not username:
            flash("필수 항목이 비었습니다.", "danger")
            return redirect(url_for("register"))
        if raw_password != confirm_password:
            flash("비밀번호가 일치하지 않습니다.", "danger")
            return redirect(url_for("register"))

        hashed_pw = generate_password_hash(raw_password)
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM USER WHERE Usercode=%s", (usercode,))
                if cursor.fetchone():
                    flash("이미 존재하는 아이디입니다.", "danger")
                    return redirect(url_for("register"))

                sql = """
                    INSERT INTO USER (Usercode, User_name, Afflication_ID, Field, Tank_ID, Password)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    sql, (usercode, username, affiliation_id, field, tank_id, hashed_pw)
                )
                conn.commit()
                flash("회원가입이 완료되었습니다.", "success")
                return redirect(url_for("index"))
        except Exception as e:
            print(f"[회원가입 오류] {e}")
            flash("회원가입 중 오류가 발생했습니다.", "danger")
            return redirect(url_for("register"))
        finally:
            conn.close()

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usercode = request.form.get("username", "").strip()
        raw_password = request.form.get("password", "")

        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT Usercode, Password FROM USER WHERE Usercode=%s", (usercode,)
                )
                row = cursor.fetchone()
                if not row or not check_password_hash(row["Password"], raw_password):
                    flash("아이디 또는 비밀번호가 올바르지 않습니다.", "danger")
                    return redirect(url_for("login"))

                session.permanent = True
                session["user"] = row["Usercode"]
                return redirect(url_for("dashboard"))
        except Exception as e:
            print(f"[로그인 오류] {e}")
            flash("로그인 중 오류가 발생했습니다.", "danger")
            return redirect(url_for("login"))
        finally:
            conn.close()

    # ⚠ 필요에 맞게 템플릿 파일명 수정(예: 'index.html'을 사용 중이면 변경)
    return render_template("index.html")

@app.route("/main")
def main():
    if "user" not in session:
        return redirect(url_for("index"))
    return render_template("main.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/detect", methods=["POST"])
def detect():
    if "user" not in session:
        return redirect(url_for("index"))

    if "video" not in request.files:
        flash("비디오 파일이 업로드되지 않았습니다.", "danger")
        return redirect(url_for("main"))

    video = request.files["video"]
    if not video.filename:
        flash("파일명이 비어 있습니다.", "danger")
        return redirect(url_for("main"))

    filename = secure_filename(video.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    video.save(filepath)

    result = detect_and_return_summary(filepath)  # dict 또는 결과 객체 가정
    return render_template("main.html", result=result)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("main_tank_view.html")

# =========================
# React SPA 서빙 (/app/*)
# =========================
# Vite 빌드(dist)를 backend/static/app/ 로 복사해 두었을 때 동작
@app.route("/app/")
@app.route("/app/<path:path>")
def serve_app(path="index.html"):
    full = os.path.join(APP_DIST, path)
    if os.path.isfile(full):
        # js/css/img 같은 정적 파일은 그대로 서빙
        return send_from_directory(APP_DIST, path)
    # 라우트 새로고침 대응: 항상 SPA 엔트리 반환
    return send_from_directory(APP_DIST, "index.html")

# =========================
# JSON API (/api/*) - React 연동
# =========================
@app.post("/api/auth/register")
def api_register():
    data = request.get_json(silent=True) or {}
    usercode = (data.get("userid") or data.get("username") or "").strip()
    raw_password = data.get("password") or ""
    username = (data.get("name") or "").strip()
    affiliation_id = (data.get("unit") or "").strip()
    tank_id = (data.get("tank") or "").strip()
    field = (data.get("rank") or "").strip()

    if not usercode or not raw_password or not username:
        return jsonify({"ok": False, "error": "missing fields"}), 400

    hashed_pw = generate_password_hash(raw_password)
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM USER WHERE Usercode=%s", (usercode,))
            if cursor.fetchone():
                return jsonify({"ok": False, "error": "user exists"}), 409

            sql = """
                INSERT INTO USER (Usercode, User_name, Afflication_ID, Field, Tank_ID, Password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                sql, (usercode, username, affiliation_id, field, tank_id, hashed_pw)
            )
            conn.commit()
        return jsonify({"ok": True}), 201
    except Exception as e:
        print(f"[API register error] {e}")
        return jsonify({"ok": False, "error": "server error"}), 500
    finally:
        conn.close()

@app.post("/api/auth/login")
def api_login():
    data = request.get_json(silent=True) or {}
    usercode = (data.get("userid") or data.get("username") or "").strip()
    raw_password = data.get("password") or ""

    if not usercode or not raw_password:
        return jsonify({"ok": False, "error": "missing fields"}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT Usercode, Password FROM USER WHERE Usercode=%s", (usercode,)
            )
            row = cursor.fetchone()
            if not row or not check_password_hash(row["Password"], raw_password):
                return jsonify({"ok": False, "error": "invalid credentials"}), 401

        # 세션 유지(필요 시 JWT로 교체 가능)
        session.permanent = True
        session["user"] = usercode
        return jsonify({"ok": True, "user": {"usercode": usercode}}), 200
    except Exception as e:
        print(f"[API login error] {e}")
        return jsonify({"ok": False, "error": "server error"}), 500
    finally:
        conn.close()

@app.post("/api/detect")
def api_detect():
    # 공개 API로 쓸 거면 아래 세 줄 주석 유지
    # if "user" not in session:
    #     return jsonify({"ok": False, "error": "unauthorized"}), 401

    if "file" not in request.files:
        return jsonify({"ok": False, "error": "file required"}), 400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"ok": False, "error": "empty filename"}), 400

    filename = secure_filename(f.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    f.save(filepath)

    try:
        result = detect_and_return_summary(filepath)  # dict 가정
        return jsonify({"ok": True, "result": result}), 200
    except Exception as e:
        print(f"[API detect error] {e}")
        return jsonify({"ok": False, "error": "inference error"}), 500

@app.get("/api/health")
def api_health():
    return jsonify({"status": "ok"}), 200

# =========================
# 실행
# =========================
if __name__ == "__main__":
    # 개발 기본 포트는 5000 (React dev server는 5173)
    app.run(host="0.0.0.0", port=5000, debug=True)
