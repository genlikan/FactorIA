import pyttsx3
from queue import Queue

tts_queue = Queue()

class _TTS:
    def __init__(self):
        self.engine = pyttsx3.init()

    def start(self, text_):
        self.engine.say(text_)
        self.engine.runAndWait()

def speak_response(text):
    tts_queue.put(text)

def tts_worker():
    while True:
        text = tts_queue.get()
        if text is None:
            break
        print(f"TTS Worker processing: {text}")
        tts = _TTS()
        tts.start(text)
        del tts
        print("Task is now done.")
        tts_queue.task_done()
