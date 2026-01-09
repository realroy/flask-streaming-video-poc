import os
from flask import Flask, request, Response, render_template

# Get the base directory (parent of api folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHUNK_SIZE = 1024 * 200  # chunks size

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)


@app.route('/')
def home():
    """Render the home page with video player and controls."""
    return render_template('index.html')


def stream_video(video_path, start, end):
    """Generator function to stream video in chunks."""
    with open(video_path, 'rb') as f:
        f.seek(start)
        remaining = end - start + 1
        while remaining > 0:
            chunk_size = min(CHUNK_SIZE, remaining)
            data = f.read(chunk_size)
            if not data:
                break
            remaining -= len(data)
            yield data


@app.route('/api/v1/avatar')
def avatar():
    """
    Stream avatar video based on state parameter with HTTP Range support.
    
    Query Parameters:
        state: 'nodding' or 'speaking'
    
    Returns:
        MP4 video stream with support for range requests (seeking)
    """
    state = request.args.get('state')
    
    if state not in ['nodding', 'speaking']:
        return {'error': 'Invalid state. Use "nodding" or "speaking".'}, 400
    
    video_path = os.path.join(BASE_DIR, 'static', 'videos', f'avatar-{state}.mp4')
    
    if not os.path.exists(video_path):
        return {'error': f'Video file not found: avatar-{state}.mp4'}, 404
    
    file_size = os.path.getsize(video_path)
    range_header = request.headers.get('Range')
    
    if range_header:
        # Parse Range header (e.g., "bytes=0-1024")
        byte_range = range_header.replace('bytes=', '').split('-')
        start = int(byte_range[0])
        end = int(byte_range[1]) if byte_range[1] else file_size - 1
        
        # Ensure end doesn't exceed file size
        end = min(end, file_size - 1)
        content_length = end - start + 1
        
        headers = {
            'Content-Type': 'video/mp4',
            'Content-Range': f'bytes {start}-{end}/{file_size}',
            'Accept-Ranges': 'bytes',
            'Content-Length': content_length,
        }
        
        return Response(
            stream_video(video_path, start, end),
            status=206,  # Partial Content
            headers=headers,
            mimetype='video/mp4'
        )
    else:
        # No range requested, stream entire file
        headers = {
            'Content-Type': 'video/mp4',
            'Accept-Ranges': 'bytes',
            'Content-Length': file_size,
        }
        
        return Response(
            stream_video(video_path, 0, file_size - 1),
            status=200,
            headers=headers,
            mimetype='video/mp4'
        )


if __name__ == '__main__':
    app.run(debug=True)
