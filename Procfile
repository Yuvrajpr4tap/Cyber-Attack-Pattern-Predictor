release: cd frontend && npm install && npm run build && cd ..
web: gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app
