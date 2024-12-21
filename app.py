import os
from flask import Flask, send_from_directory

# Initialize Flask app
app = Flask(__name__)

# Folder to store the HTML files
html_folder = './html_files/'

# Create folder if it doesn't exist
if not os.path.exists(html_folder):
    os.makedirs(html_folder)

# Function to serve the HTML file
@app.route('/<filename>')
def serve_html(filename):
    return send_from_directory(html_folder, filename)

if __name__ == '__main__':
    # Run Flask app
    app.run(host='0.0.0.0', port=5000)
