from flask import Flask, request, render_template, redirect, url_for, session, flash
import tempfile
import os
import assemblyai as aai
from dotenv import load_dotenv
from flask_session import Session

# Load environment variables
load_dotenv()
api_key = os.getenv('ASSEMBLYAI_API_KEY')
aai.settings.api_key = api_key

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Set a secret key for security purposes
app.config['SESSION_TYPE'] = 'filesystem'  # Specifies the session type to use
Session(app)  # Initialize session

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

    # Create a temporary file in the system's temp directory
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    file_path = temp_file.name
    file.save(file_path)
    temp_file.close()  # Explicitly close the file handle

    session['file_path'] = file_path  # Store the file path in the session
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
            return render_template('transcription.html', transcript=transcript.text, error=None)
    finally:
        # Ensure the temporary file is deleted after processing
        os.remove(file_path)
        session.pop('file_path', None)  # Remove the file path from the session

if __name__ == '__main__':
    app.run(debug=True)
