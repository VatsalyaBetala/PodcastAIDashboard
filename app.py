from flask import Flask, request, render_template
import assemblyai as aai

app = Flask(__name__)
api_key = 'Your API Key'
aai.settings.api_key = api_key

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
        file_path = f'./{file.filename}'
        file.save(file_path)

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path)

        if transcript.status == aai.TranscriptStatus.error:
            error_message = transcript.error
            return render_template('transcription.html', error=error_message, transcript=None)
        else:
            return render_template('transcription.html', transcript=transcript.text, error=None)

if __name__ == '__main__':
    app.run(debug=True)
