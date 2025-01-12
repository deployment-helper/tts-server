# tts-server
Text to speech server

## Run production server 
```bash
gunicorn --bind 0.0.0.0:8080 --config gunicorn.conf.py  -w 4 --threads 10 app:app
```