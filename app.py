import base64
import logging
import io
import uuid
from threading import Semaphore
from dotenv import load_dotenv

from flask import Flask, render_template, request, send_file, jsonify

from TTS.utils.synthesizer import Synthesizer
from TTS.utils.manage import ModelManager

from s3_reader import read_file_from_s3, delete_os_file

XTTS_V2 = "tts_models/multilingual/multi-dataset/xtts_v2"
MAX_REQUEST_SIZE = 1
TEMP_PATH = '/tmp'

# load environment variables
load_dotenv()

sem = Semaphore(MAX_REQUEST_SIZE)
manager = ModelManager('./.models.json')
model_path, config_path, model_item = manager.download_model(XTTS_V2)

synthesizer = Synthesizer(
    tts_checkpoint=model_path,
    # config path is none for already downloaded models as it is saved in the model folder.
    # we are setting config path manually here.
    tts_config_path=f"{model_path}/config.json",
    tts_speakers_file=None,
    tts_languages_file=None,
    vocoder_checkpoint="",
    vocoder_config="",
    encoder_checkpoint="",
    encoder_config="",
    use_cuda=False,
)

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Routes
@app.route('/')
def index():
    return  render_template('index.html')
@app.route('/health')
def health():
    return "OK"

@app.route('/api/models', methods=['GET'])
def api_models():

    return jsonify(manager.list_tts_models())

@app.route('/api/synthesize', methods=['POST','OPTIONS'])
def api_synthesize():
    data = request.get_json()
    text = data['text']
    send_as_file = data.get('send_as_file', False)
    speaker = data.get('speaker', 'Tanja Adelina')
    language = data.get('language', 'en')
    # Speaker_ref is S3 key path to clone the voice of this speaker.
    speaker_ref = data.get('speaker_ref', None)
    logging.log(logging.INFO, f"Synthesizing: {text}")

    if speaker_ref:
        # Download the speaker reference file from S3
        speaker_ref_file = f"{TEMP_PATH}/{uuid.uuid4()}.wav"
        read_file_from_s3( speaker_ref, speaker_ref_file)

    sem.acquire()

    try:
        if speaker_ref:
            wavs = synthesizer.tts(text, language_name=language, speaker_name=None, speaker_wav=speaker_ref_file)
        else:
            wavs = synthesizer.tts(text, language_name=language, speaker_name=speaker)

        out = io.BytesIO()
        synthesizer.save_wav(wavs, out)
        if send_as_file:
            out.seek(0)
            return send_file(out, mimetype="audio/wav")
        else:
            out.seek(0)
            audio_content = base64.b64encode(out.getvalue()).decode('utf-8')
            logging.log(logging.INFO, f"Synthesized: {audio_content}")
            return jsonify({"audioContent": audio_content})
    finally:
        if speaker_ref:
            delete_os_file(speaker_ref_file)
        sem.release()
# Main entry point
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True,threaded=True)