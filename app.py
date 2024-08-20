from flask import Flask, request, render_template, redirect, url_for
import tempfile
import os
import assemblyai as aai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('ASSEMBLYAI_API_KEY')
aai.settings.api_key = api_key

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return "No file part in the request", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected for uploading", 400

    if file:
        # Create a temporary file in the system's temp directory
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        file_path = temp_file.name
        file.save(file_path)
        temp_file.close()  # Explicitly close the file handle

        try:
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(file_path)

            if transcript.status == aai.TranscriptStatus.error:
                error_message = transcript.error
                return render_template('transcription.html', error=error_message, transcript=None)
            else:
                return render_template('transcription.html', transcript=transcript.text, error=None)
        finally:
            # Ensure the temporary file is deleted after processing
            os.remove(file_path)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
