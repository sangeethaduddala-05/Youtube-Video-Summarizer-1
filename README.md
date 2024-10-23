# Youtube-Video-Summarizer
The YouTube Summarizer is an AI-powered tool that automatically generates concise summaries of YouTube videos by utilizing their transcripts. Built with a user-friendly interface using Streamlit, this project allows users to input a YouTube video link, extract the transcript using the YouTube Transcript API, and summarize it using advanced natural language processing (NLP) models from Google Gemini Pro. This summarization makes it easy to understand the core points of a video within 250 words, eliminating the need to watch lengthy videos. The application can handle a wide range of content, providing fast and accurate summaries even for videos without detailed descriptions.

The project integrates several key technologies. Python serves as the primary programming language, offering flexibility for handling API requests, text processing, and data integration. The YouTube Transcript API extracts the raw transcript text from videos, while Google Gemini Pro (part of Google Generative AI) is used to perform the summarization. Environment variables such as API keys are securely managed using the python-dotenv library. The Streamlit framework enables a smooth web-based interface where users can easily interact with the summarizer. The project also incorporates pathlib for streamlined file handling. Overall, this project showcases the powerful combination of APIs and machine learning models in simplifying content consumption.

**Technologies Used:**

**Python:**
The core programming language used to develop the application, handling API interactions, text processing, and data flow.

**Streamlit:**
A Python framework that enables building the web-based interface for the summarizer, allowing users to input YouTube links and view the results in a simple and interactive UI.

**YouTube Transcript API:**
This API fetches the transcript from YouTube videos, providing the raw text needed for summarization.

**Google Generative AI (Gemini Pro):**
A powerful NLP model that processes the video transcript and generates a concise summary of the content in a clear and readable format.
python-dotenv:
A library used to manage environment variables like API keys securely, ensuring sensitive data like the Google API Key is kept confidential.

**Pathlib:**
A Python library used for handling and managing file paths, making the code more robust and portable.

