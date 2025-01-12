# tts-server
Text to speech server



## Run production server 
```bash
gunicorn --bind 0.0.0.0:8080 --config gunicorn.conf.py  -w 4 --threads 10 app:app
```

## Update HTTP server(node.js)
Need add environment variable 
`TTS_SERVER_URL=http://127.0.0.1:8080` 