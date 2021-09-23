import os
import time


def read_file(input_file):
    input_file.seek(0, os.SEEK_END)
    while True:
        content = input_file.readline()
        # Added sleep time to reduce computation power.
        # If processing power is not an issue for the machine remove time.sleep() call.
        if not content:
            time.sleep(0.1)
            continue
        yield content
