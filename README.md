# tts-server
Text to speech server



## Run production server 
```bash
gunicorn --bind 0.0.0.0:8080 --config gunicorn.conf.py  -w 4 --threads 10 app:app
```

## Update HTTP server(node.js)
Need add environment variable 
`TTS_SERVER_URL=http://127.0.0.1:8080` 

# How to run production server 

To run a Gunicorn server in a tmux session and expose it to the public using ngrok, follow these steps:

1. Install tmux (if not already installed)

If tmux is not installed, install it using Homebrew:

`brew install tmux`

Verify the installation:

`tmux -V`

2. Start a tmux Session

Start a new tmux session to run your Gunicorn server:

`tmux new -s gunicorn_server`

This opens a new tmux session named gunicorn_server.

3. Run Gunicorn

Start the Gunicorn server inside the tmux session. Replace my_app:app with the correct module and application object for your project.

Example:

Set environment variables in this session:

`caffeinate -dims &  gunicorn -w 4 -b 127.0.0.1:8080 my_app:app`

This starts Gunicorn with:
	•	-w 4: 4 worker processes.
	•	-b 127.0.0.1:8080: Binds the server to localhost on port 8080.

You can test your Gunicorn server locally:

http://127.0.0.1:8080

4. Detach the tmux Session

Detach from the tmux session while keeping Gunicorn running by pressing:

Ctrl + B, then D

This takes you back to the terminal, but your Gunicorn server continues running in the background.

5. Attach ngrok to the Gunicorn Server

Now, start ngrok to expose the Gunicorn server to the public:

`caffeinate -dims & ngrok http 8080`

This will generate a public URL like:

Forwarding                    https://<random-id>.ngrok.io -> http://127.0.0.1:8080

You can share this public URL, and ngrok will forward the traffic to your Gunicorn server.

6. Reattach the tmux Session

If you need to return to the Gunicorn tmux session to view logs or stop the server, reattach it using:

`tmux attach -t gunicorn_server`

7. Optional: Run Both Gunicorn and ngrok in tmux

If you prefer to run both Gunicorn and ngrok in the same or separate tmux sessions:

In the Same Session:
	1.	Open a tmux session:

`tmux new -s my_services`


	2.	Run Gunicorn:

`gunicorn -w 4 -b 127.0.0.1:8080 my_app:app`


	3.	Split the tmux window:
Press Ctrl + B, then % (splits the window vertically).
	4.	Run ngrok in the new pane:

`ngrok http 8080`



In Separate Sessions:
	1.	Start a session for Gunicorn:

tmux new -s gunicorn_server

Run Gunicorn, then detach (Ctrl + B, D).

	2.	Start another session for ngrok:

tmux new -s ngrok

Run ngrok, then detach.

This setup ensures both your Gunicorn server and ngrok are running in the background and accessible anytime! Let me know if you face any issues.