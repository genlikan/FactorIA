import pyaudio
import wave
import os
import subprocess
import whisper
from model import generate_response
from text_to_speech import speak_response, tts_queue

model = whisper.load_model("base")

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

def recognize_speech_from_audio(filename):
    try:
        result = model.transcribe(filename)
        return result["text"]
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return ""

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

DEVICE_INDEX_FILE = "device_index.txt"

def save_device_index(index):
    with open(DEVICE_INDEX_FILE, 'w') as f:
        f.write(str(index))

def load_device_index():
    if os.path.exists(DEVICE_INDEX_FILE):
        with open(DEVICE_INDEX_FILE, 'r') as f:
            return int(f.read().strip())
    return None

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
                    print(f"Llama response: {response}")
                    speak_response(response)
                    tts_queue.join()  # Ensure the TTS queue is processed

        else:
            print("Audio file not found. Please check the recording process.")
