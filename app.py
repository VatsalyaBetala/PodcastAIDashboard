# app.py

from flask import Flask, request, jsonify
import tempfile
import os
import assemblyai as aai
from dotenv import load_dotenv
from transformers import pipeline
from keybert import KeyBERT
from flask_cors import CORS

# Load environment variables
load_dotenv()
api_key = os.getenv('ASSEMBLYAI_API_KEY')
if not api_key:
    raise ValueError("Please set your ASSEMBLYAI_API_KEY in the .env file")
aai.settings.api_key = api_key

app = Flask(__name__)
CORS(app)

# Initialize NLP Models
summarizer = pipeline('summarization', model="facebook/bart-large-cnn")
sentiment_analyzer = pipeline('sentiment-analysis')
kw_model = KeyBERT()

@app.route('/api/upload', methods=['POST'])
def upload_audio():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected for uploading'}), 400

        # Save the uploaded file to a temporary location
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        file_path = temp_file.name
        file.save(file_path)
        temp_file.close()

        # Transcribe the audio file using AssemblyAI
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path)

        if transcript.status == aai.TranscriptStatus.error:
            return jsonify({'error': f"Transcription error: {transcript.error}"}), 500

        transcript_text = transcript.text

        # Summarize the transcript
        summary = summarizer(transcript_text, max_length=150, min_length=30, do_sample=False)
        summary_text = summary[0]['summary_text']

        # Generate hashtags using KeyBERT
        keywords = kw_model.extract_keywords(
            transcript_text,
            keyphrase_ngram_range=(1, 2),
            stop_words='english',
            top_n=10
        )
        hashtags = ['#' + keyword[0].replace(' ', '') for keyword in keywords]

        # Perform sentiment analysis
        sentiment = sentiment_analyzer(transcript_text)
        sentiment_label = sentiment[0]['label']
        sentiment_score = sentiment[0]['score']

        # Return the results as JSON
        return jsonify({
            'transcript': transcript_text,
            'summary': summary_text,
            'hashtags': hashtags,
            'sentiment': {
                'label': sentiment_label,
                'score': sentiment_score
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(debug=True)
