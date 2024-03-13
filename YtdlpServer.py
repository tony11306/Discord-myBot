import re
from flask import Flask, jsonify, request
import yt_dlp

app = Flask(__name__)

@app.route('/songs', methods=['POST'])
def get_songs():
    print(request.json)
    query = request.json['query']
    ydl_opts = {
        'format': 'bestaudio',
        'title': True,
        'quiet': True,
        'no_warnings': True,
        "skip_download": True,
        "ignoreerrors": True,
        "extract_flat": True,
    }
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, query): # If the query is a URL
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            return jsonify(info)
    else:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl_opts['extract_flat'] = False
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            return jsonify(info)
        
if __name__ == '__main__':
    app.run(debug=False)