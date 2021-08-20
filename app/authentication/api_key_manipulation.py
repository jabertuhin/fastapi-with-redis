from datetime import datetime
from typing import NewType

Seconds = NewType("Seconds", int)

def get_api_key_with_time(api_key: str,  time: Seconds) -> str:
    # Based on minute.
    if time//60 == 1:
        return f"{api_key}:{str(datetime.now().minute)}"

    raise ValueError("Doesn't support other than minute(60 seconds).")