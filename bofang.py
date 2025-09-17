import requests, pyaudio, json


def tts_stream(text: str):
    payload = {
        "cha_name": "nahida",
        "text": text,
        "text_language": "多语种混合",
        "character_emotion": "default",
        "batch_size": 1,
        "stream": True
    }

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=32000,
                    output=True,
                    frames_per_buffer=1024)

    resp = requests.post("http://127.0.0.1:5000/tts", json=payload, stream=True)
    for chunk in resp.iter_content(chunk_size=1024):
        if chunk:
            stream.write(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()


# 使用
if __name__ == "__main__":
    tts_stream("你好，这是可变文本")
