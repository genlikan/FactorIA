import os
import threading
from queue import Queue

from init_db import setup_database
from game_api import get_player_name

from audio_utils import list_audio_devices, save_device_index, load_device_index, listen_and_transcribe, check_ffmpeg
from text_to_speech import speak_response, tts_worker

# from todo import setup_database
# from reminder import start_reminder_thread


def main():
    setup_database()

    print("Listing all available audio input devices:")
    devices = list_audio_devices()

    if not devices:
        print("No audio input devices found.")
        return

    device_index = load_device_index()
    if device_index is None:
        device_index = int(input("Enter the device index you want to use: "))
        save_device_index(device_index)
    else:
        print(f"Using saved device index: {device_index}")

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