# Model: https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-english

from asrecognition import ASREngine

asr = ASREngine("en", model_path="jonatasgrosman/wav2vec2-large-xlsr-53-english")

AUDIO_IN = "./audios/mouth.mp3"

audio_paths = [AUDIO_IN]
transcription = asr.transcribe(audio_paths)[0]["transcription"]
print(transcription)

from playsound import playsound
playsound(AUDIO_IN)

