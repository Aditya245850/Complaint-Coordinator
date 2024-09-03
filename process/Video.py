import os
from google.cloud import videointelligence_v1 as videointelligence

from helper.Categorizer import categorizer
from helper.SentimentAnalysis import sentimentAnalysis
from helper.StoreIntoDatabase import storeIntoDatabase
from helper.Summary import video_summarizer

def process_Video(file_path, username, API_KEY):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "path_to_json"

    with open(file_path, "rb") as video_file:
        content = video_file.read()

    client = videointelligence.VideoIntelligenceServiceClient()


    features = [
        videointelligence.Feature.LABEL_DETECTION,
        videointelligence.Feature.TEXT_DETECTION,
        videointelligence.Feature.OBJECT_TRACKING,
        videointelligence.Feature.SPEECH_TRANSCRIPTION
    ]

    operation = client.annotate_video(
        request={"features": features, "input_content": content}
    )

    result = operation.result(timeout=600)

    video_details = []

    video_details.append("Label Detection Results:\n")
    for annotation in result.annotation_results[0].segment_label_annotations:
        label_info = f"Label: {annotation.entity.description}\n"
        for segment in annotation.segments:
            label_info += f"  Start: {segment.segment.start_time_offset}, End: {segment.segment.end_time_offset}\n"
        video_details.append(label_info)

    video_details.append("\nText Detection Results:\n")
    for text_annotation in result.annotation_results[0].text_annotations:
        text_info = f"Text: {text_annotation.text}\n"
        for segment in text_annotation.segments:
            text_info += f"  Start: {segment.segment.start_time_offset}, End: {segment.segment.end_time_offset}\n"
            text_info += f"  Confidence: {segment.confidence}\n"
        video_details.append(text_info)

    video_details.append("\nObject Tracking Results:\n")
    for annotation in result.annotation_results[0].object_annotations:
        object_info = f"Object: {annotation.entity.description}\n"
        object_info += f"  Start: {annotation.segment.start_time_offset}, End: {annotation.segment.end_time_offset}\n"
        video_details.append(object_info)

    video_details.append("\nSpeech Transcription Results:\n")
    for speech_transcription in result.annotation_results[0].speech_transcriptions:
        for alternative in speech_transcription.alternatives:
            speech_info = f"Transcript: {alternative.transcript}\n"
            speech_info += f"Confidence: {alternative.confidence}\n"
            video_details.append(speech_info)

    video_analysis = "".join(video_details)

    summary = video_summarizer(video_analysis, API_KEY)

    category = categorizer(summary, API_KEY)

    sentiment = sentimentAnalysis(video_analysis)

    storeIntoDatabase(summary, category, sentiment, username)
