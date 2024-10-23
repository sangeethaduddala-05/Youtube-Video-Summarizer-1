import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from googletrans import Translator
# Load environment variables
load_dotenv()

# Configure Google Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define prompt template
prompt_template = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video. Your summary should include detailed explanations for each 45-second interval, 
limited to 3-4 lines. Please provide the summary of the text given here: """


# Function to extract transcript details with timestamps
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi', 'te'])
        return transcript_list
    except NoTranscriptFound:
        st.error("No transcript found for the video.")
        return None
    except TranscriptsDisabled:
        st.error("Transcripts are disabled for this video.")
        return None
    except Exception as e:
        st.error(f"Error extracting transcript: {e}")
        return None


# Function to translate transcript to English if necessary
def translate_transcript(transcript_list, target_language="en"):
    try:
        translator = Translator()
        translated_transcript = []
        for item in transcript_list:
            translation = translator.translate(item["text"], dest=target_language).text
            translated_transcript.append({"start": item["start"], "text": translation})
        return translated_transcript
    except Exception as e:
        st.error(f"Error translating transcript: {e}")
        return transcript_list


# Aggregate transcript text for each 45-second interval
def aggregate_transcript(transcript_list, interval=45):
    aggregated_transcript = []
    current_interval = 0
    current_text = []

    for item in transcript_list:
        if item['start'] >= current_interval + interval:
            aggregated_transcript.append({
                "timestamp": current_interval,
                "text": " ".join(current_text)
            })
            current_interval += interval
            current_text = []

        current_text.append(item['text'])

    # Add the last interval
    if current_text:
        aggregated_transcript.append({
            "timestamp": current_interval,
            "text": " ".join(current_text)
        })

    return aggregated_transcript


# Function to generate content using Google Gemini
def generate_gemini_content(aggregated_transcript, prompt):
    try:
        detailed_notes = []
        model = genai.GenerativeModel("gemini-pro")

        for segment in aggregated_transcript:
            segment_prompt = prompt + segment['text']

            # Adjust max_tokens based on desired summary length (approx. 3-4 lines)
            response = model.generate_content(segment_prompt, max_tokens=150)

            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content'):
                    detailed_notes.append({
                        "timestamp": segment['timestamp'],
                        "summary": candidate.content
                    })
                else:
                    detailed_notes.append({
                        "timestamp": segment['timestamp'],
                        "summary": "Summary not available due to API response issues."
                    })
            else:
                detailed_notes.append({
                    "timestamp": segment['timestamp'],
                    "summary": "Summary not available due to API response issues."
                })

        return detailed_notes
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None


# Convert timestamp to a more readable format
def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


# Streamlit interface
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("v=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_list = extract_transcript_details(youtube_link)
    if transcript_list:
        translated_transcript = translate_transcript(transcript_list)
        aggregated_transcript = aggregate_transcript(translated_transcript, interval=45)

        st.markdown("## Transcript with Timestamps:")
        for segment in aggregated_transcript:
            st.write(f"{format_timestamp(segment['timestamp'])}: {segment['text']}")

        detailed_notes = generate_gemini_content(aggregated_transcript, prompt_template)

        if detailed_notes:
            st.markdown("## Detailed Notes:")
            for note in detailed_notes:
                st.write(f"{format_timestamp(note['timestamp'])}: {note['summary']}")