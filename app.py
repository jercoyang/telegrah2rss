from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
import os
import uuid
from rss_utils import process_rss_from_url, process_rss_from_file
from update_scheduler import start_scheduler, rss_jobs
from db import init_db, save_job
import threading

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'processed'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化数据库
init_db()

# 启动调度器（确保只启动一次）
scheduler_started = False

def ensure_scheduler_started():
    global scheduler_started
    if not scheduler_started:
        start_scheduler()
        scheduler_started = True

# 在应用启动时启动调度器
ensure_scheduler_started()

@app.route("/", methods=["GET", "POST"])
def index():
    ensure_scheduler_started()
    if request.method == "POST":
        input_url = request.form.get("rss_url")
        file = request.files.get("rss_file")

        uid = str(uuid.uuid4())
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uid}.xml")

        if input_url:
            success = process_rss_from_url(input_url, output_path)
            if success:
                rss_jobs[uid] = input_url
                save_job(uid, input_url, "url")
                return redirect(url_for("view_rss", uid=uid))
        elif file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            process_rss_from_file(file_path, output_path)
            rss_jobs[uid] = f"file:{filename}"
            save_job(uid, f"file:{filename}", "file")
            return redirect(url_for("view_rss", uid=uid))

    return render_template("index.html")

@app.route("/rss/<uid>.xml")
def view_rss(uid):
    return send_from_directory(app.config['UPLOAD_FOLDER'], f"{uid}.xml", mimetype="application/rss+xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)