import os

workers = int(os.environ.get("GUNICORN_WORKERS", 2))
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
timeout = 120
worker_class = "sync"
