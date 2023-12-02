import time
import uuid
import pyperclip

if __name__ == "__main__":
    while True:
        generated = uuid.uuid4()
        print(f"uuid: {generated}")
        pyperclip.copy(f"\"{generated}\": {{}}")
        time.sleep(0.1)
