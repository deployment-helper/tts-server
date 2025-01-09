import logging
import io
from TTS.utils.synthesizer import Synthesizer
from TTS.utils.manage import ModelManager
from flask import Flask, render_template, request, send_file, jsonify

XTTS_V2 = "tts_models/multilingual/multi-dataset/xtts_v2"

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

@app.route('/api/synthesize', methods=['POST'])
def api_synthesize():
    data = request.get_json()
    text = data['text']
    speaker = data.get('speaker', None)
    language = data.get('language', None)
    logging.log(logging.INFO, f"Synthesizing: {text}")
    wavs = synthesizer.tts(text, language_name=language, speaker_name=speaker)
    out = io.BytesIO()
    synthesizer.save_wav(wavs, out)
    return send_file(out, mimetype="audio/wav")
# Main entry point
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)