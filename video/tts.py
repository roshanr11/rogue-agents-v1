"""Text-to-speech through OpenRouter (openai/gpt-audio-mini, audio output via streamed chat completions).
    python video/tts.py "text" out.wav
"""
import base64, json, sys, urllib.request, wave

def tts(text, out, voice="alloy", model="openai/gpt-audio-mini"):
    body = json.dumps({"model": model, "modalities": ["text", "audio"], "stream": True,
        "audio": {"voice": voice, "format": "pcm16"},
        "messages": [{"role": "system", "content": "You are a voiceover narrator. Read the user's text aloud exactly as written, word for word, in an energetic, clear hackathon-demo tone. Do not add or change any words."},
                     {"role": "user", "content": text}]}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer sk-or-proxy-injected"})
    pcm, transcript = bytearray(), []
    with urllib.request.urlopen(req, timeout=180) as r:
        for line in r:
            line = line.decode().strip()
            if not line.startswith("data: ") or line == "data: [DONE]":
                continue
            d = json.loads(line[6:])
            for ch in d.get("choices", []):
                a = (ch.get("delta") or {}).get("audio") or {}
                if a.get("data"):
                    pcm += base64.b64decode(a["data"])
                if a.get("transcript"):
                    transcript.append(a["transcript"])
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(bytes(pcm))
    return "".join(transcript), len(pcm) / 48000

if __name__ == "__main__":
    t, secs = tts(sys.argv[1], sys.argv[2])
    print(f"{secs:.1f}s | {t}")
