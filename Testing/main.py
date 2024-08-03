import whisper
import pyaudio
import wave
import os
import subprocess
import threading
from queue import Queue
from init_db import setup_database
from game_api import get_player_name
from model import generate_response
import pyttsx3
# from todo import setup_database
# from reminder import start_reminder_thread

# Load the Whisper model
model = whisper.load_model("base")

# Function to check if FFmpeg is installed
def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

# Function to recognize speech from audio file
def recognize_speech_from_audio(filename):
    try:
        result = model.transcribe(filename)
        return result["text"]
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return ""

# Function to record audio from the microphone
def record_audio(device_index, filename, duration=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = duration
    WAVE_OUTPUT_FILENAME = filename

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=CHUNK)

    print("Listening...")
    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to list all audio input devices
def list_audio_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    device_list = []

    for i in range(0, numdevices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            device_list.append((i, device_info.get('name')))
            print(f"Device index {i}: {device_info.get('name')}")
    
    p.terminate()
    return device_list

# TTS Class Definition
class _TTS:
    def __init__(self):
        self.engine = pyttsx3.init()

    def start(self, text_):
        self.engine.say(text_)
        self.engine.runAndWait()

# Function to speak a text response
def speak_response(text):
    tts_queue.put(text)

# Text-to-speech thread function
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

# Main function to handle the voice wake command and other functionalities
def listen_and_transcribe(device_index):
    while True:
        # Record audio for wake word
        record_audio(device_index, "wake_word.wav", duration=2)

        # Check if the file exists
        if os.path.exists("wake_word.wav"):
            # Transcribe the recorded audio for wake word
            transcription = recognize_speech_from_audio("wake_word.wav").lower().strip()
            print(f"You said: {transcription}")

            if transcription.startswith("listen"):
                # Acknowledge wake word
                speak_response("I'm listening")
                tts_queue.join()  # Ensure the TTS queue is processed

                # Record longer duration for user's query
                record_audio(device_index, "query.wav", duration=5)
                
                if os.path.exists("query.wav"):
                    # Transcribe the recorded query
                    query_transcription = recognize_speech_from_audio("query.wav").lower().strip()
                    print(f"Your question: {query_transcription}")

                    if query_transcription == "exit":
                        print("Exit command detected. Shutting down.")
                        speak_response("Goodbye!")
                        tts_queue.join()  # Ensure the TTS queue is processed
                        break

                    # Generate response using Llama model
                    response = generate_response(query_transcription)
                    print(type(response))
                    print(response[0]["arguments"]["content"])
                    response = response[0]["arguments"]["content"]
                    print(f"Llama response: {response}")
                    speak_response(response)
                    tts_queue.join()  # Ensure the TTS queue is processed

        else:
            print("Audio file not found. Please check the recording process.")

def main():
    setup_database()

    print("Listing all available audio input devices:")
    devices = list_audio_devices()

    if not devices:
        print("No audio input devices found.")
        return

    device_index = int(input("Enter the device index you want to use: "))

    # Start the text-to-speech worker thread
    tts_thread = threading.Thread(target=tts_worker)
    tts_thread.start()

    try:
        player_name = get_player_name()
        print(f"Greetings {player_name}!")
        speak_response(f"Greetings {player_name}!")
        tts_queue.join()  # Ensure the TTS queue is processed
    except Exception as e:
        print("Game not Launched", e)
        speak_response("Game not Launched")
        tts_queue.join()  # Ensure the TTS queue is processed

    # Start the listening and transcribing process
    listen_and_transcribe(device_index)

    tts_queue.put(None)  # Signal the TTS worker to exit
    tts_thread.join()  # Wait for the TTS worker thread to finish

if __name__ == "__main__":
    if not check_ffmpeg():
        print("FFmpeg is not installed or not found in the system PATH.")
        exit()

    tts_queue = Queue()
    main()
