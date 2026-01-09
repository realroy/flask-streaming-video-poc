import os
from flask import Flask, request, send_file, render_template

# Get the base directory (parent of api folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)


@app.route('/')
def home():
    """Render the home page with video player and controls."""
    return render_template('index.html')


@app.route('/api/v1/avatar')
def avatar():
    """
    Stream avatar video based on state parameter.
    
    Query Parameters:
        state: 'nodding' or 'speaking'
    
    Returns:
        MP4 video stream or 400 error for invalid state
    """
    state = request.args.get('state')
    
    if state not in ['nodding', 'speaking']:
        return {'error': 'Invalid state. Use "nodding" or "speaking".'}, 400
    
    video_path = os.path.join(BASE_DIR, 'static', 'videos', f'avatar-{state}.mp4')
    
    if not os.path.exists(video_path):
        return {'error': f'Video file not found: avatar-{state}.mp4'}, 404
    
    return send_file(video_path, mimetype='video/mp4')


if __name__ == '__main__':
    app.run(debug=True)
