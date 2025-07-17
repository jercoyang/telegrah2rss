from apscheduler.schedulers.background import BackgroundScheduler
from rss_utils import process_rss_from_url
import os
from db import load_jobs
import threading

# 从数据库加载任务
rss_jobs = load_jobs()
scheduler = BackgroundScheduler()
scheduler_started = False
lock = threading.Lock()

def update_all_rss():
    print("Running scheduled RSS update...")
    # 创建副本避免在迭代时修改字典
    jobs_copy = rss_jobs.copy()
    for uid, url in jobs_copy.items():
        output_path = os.path.join("processed", f"{uid}.xml")
        if os.path.exists(output_path):
            print(f"Updating {url} -> {output_path}")
            if url.startswith("http"):
                try:
                    process_rss_from_url(url, output_path)
                except Exception as e:
                    print(f"Error updating {url}: {e}")
            else:
                print(f"Skipping file-based RSS: {url}")

def start_scheduler():
    global scheduler_started
    with lock:
        if not scheduler_started:
            scheduler.add_job(update_all_rss, "interval", minutes=30)
            scheduler.start()
            scheduler_started = True
            print(f"Scheduler started. Loaded {len(rss_jobs)} jobs from database.")