from openai import OpenAI
import openai
import os
def summarizer_one(file_path, API_KEY):
    client = OpenAI(api_key = API_KEY)

    with open(file_path, 'r') as file:
        complaint_content = file.read()

    chat_completion = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes complaints."},
                {"role": "user", "content": f"Please summarize the following complaint: {complaint_content}"}
        ],
        max_tokens = 150
    )
    return chat_completion.choices[0].message.content

def summarizer_two(text, API_KEY):
    client = OpenAI(api_key = API_KEY)

    chat_completion = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes complaints."},
                {"role": "user", "content": f"Please summarize the following complaint: {text}"}
        ],
        max_tokens = 150
    )
    return chat_completion.choices[0].message.content
def video_summarizer(text, API_KEY):
    client = OpenAI(api_key = API_KEY)

    chat_completion = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes complaints."},
                {"role": "user", "content": "Using the following video analysis data, create a concise summary that captures only the complaint-related content. Include relevant information derived from label tracking, object detection, text detection, and speech transcription, but omit any references to how this information was gathered or detected. Focus purely on the details that pertain to the complaint itself: {text}"}
        ],
        max_tokens = 150
    )
    return chat_completion.choices[0].message.content