import os
import librosa
import soundfile as sf
from google.cloud import speech_v1 as speech
from google.cloud.speech_v1 import RecognitionConfig, RecognitionAudio
from helper.Categorizer import categorizer
from helper.SentimentAnalysis import sentimentAnalysis
from helper.StoreIntoDatabase import storeIntoDatabase
from helper.Summary import summarizer_two

def process_Voice(file_path, username, API_KEY):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "path_to_json"

    with open(file_path, "rb") as audio_file:
        content = audio_file.read()
    
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""

    for result in response.results:
        transcript += result.alternatives[0].transcript + ' '

    transcript = transcript.strip()
    
    summary = summarizer_two(transcript, API_KEY)

    category = categorizer(summary, API_KEY)

    sentiment = sentimentAnalysis(transcript)

    storeIntoDatabase(summary, category, sentiment, username)
