from flask import Flask, render_template, request, jsonify
# Ensure both functions are imported
from downloader import download_video, get_progress 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"status": "error", "message": "No URL provided."})

    result = download_video(url)
    return jsonify(result)


@app.route('/progress', methods=['GET'])
def progress():
    # Returns the detailed status dictionary to the frontend
    return jsonify(get_progress())

if __name__ == '__main__':
    app.run(debug=True)