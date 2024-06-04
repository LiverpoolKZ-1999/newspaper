bind: str = "0.0.0.0:8000"
worker_class: str = "gevent"
workers: int = 5
max_requests: int = 64
capture_output: bool = True
max_requests_jitter: int = 64
timeout: int = 180
