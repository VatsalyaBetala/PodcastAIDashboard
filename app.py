from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
import tempfile
import os
import assemblyai as aai
from dotenv import load_dotenv
from flask_session import Session
from transformers import pipeline 

# Load environment variables
load_dotenv()
api_key = os.getenv('ASSEMBLYAI_API_KEY')
aai.settings.api_key = api_key

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Summarizer Instance
summarizer = pipeline('summarization')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        flash("No file part in the request", 'error')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash("No file selected for uploading", 'error')
        return redirect(url_for('index'))

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    file_path = temp_file.name
    file.save(file_path)
    temp_file.close()

    session['file_path'] = file_path
    return redirect(url_for('transcribe_audio'))

@app.route('/transcribe', methods=['GET'])
def transcribe_audio():
    file_path = session.get('file_path')
    if not file_path:
        flash("No file uploaded or file path missing in session", 'error')
        return redirect(url_for('index'))

    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path)

        if transcript.status == aai.TranscriptStatus.error:
            flash(f"Transcription error: {transcript.error}", 'error')
            return render_template('transcription.html', error=transcript.error, transcript=None)
        else:
            session['transcript'] = transcript.text  # Store transcript in session

            # Immediately summarize the transcript
            try:
                summary = summarizer(transcript.text, max_length=200, min_length=30, do_sample=False)
                summary_text = summary[0]['summary_text']
                return render_template('transcription.html', transcript=transcript.text, summary=summary_text, error=None)
            except Exception as e:
                flash(f"Summarization error: {str(e)}", 'error')
                return render_template('transcription.html', transcript=transcript.text, error=str(e))

    finally:
        os.remove(file_path)
        session.pop('file_path', None)

if __name__ == '__main__':
    app.run(debug=True)
