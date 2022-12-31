from datetime import datetime

def now() -> str:
    now = datetime.now()
    now_str = now.strftime("%H:%M:%S")
    return now_str
