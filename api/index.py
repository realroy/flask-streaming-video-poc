import os
from flask import Flask, request, Response, render_template

# Get the base directory (parent of api folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_CHUNK_SIZE = 1024 * 200  # 200KB default

# Valid chunk sizes in KB
VALID_CHUNK_SIZES = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1024]

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)


@app.route('/')
def home():
    """Render the home page with video player and controls."""
    return render_template('index.html')


def stream_video(video_path, start, end, chunk_size):
    """Generator function to stream video in chunks."""
    with open(video_path, 'rb') as f:
        f.seek(start)
        remaining = end - start + 1
        while remaining > 0:
            read_size = min(chunk_size, remaining)
            data = f.read(read_size)
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
        chunk_size: chunk size in KB (100, 200, 300, 400, 500, 600, 700, 800, 900, 1024)
    
    Returns:
        MP4 video stream with support for range requests (seeking)
    """
    state = request.args.get('state')
    
    if state not in ['nodding', 'speaking']:
        return {'error': 'Invalid state. Use "nodding" or "speaking".'}, 400
    
    # Parse chunk_size parameter
    chunk_size_kb = request.args.get('chunk_size', type=int)
    if chunk_size_kb and chunk_size_kb in VALID_CHUNK_SIZES:
        chunk_size = chunk_size_kb * 1024
    else:
        chunk_size = DEFAULT_CHUNK_SIZE
    
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
            stream_video(video_path, start, end, chunk_size),
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
            stream_video(video_path, 0, file_size - 1, chunk_size),
            status=200,
            headers=headers,
            mimetype='video/mp4'
        )


if __name__ == '__main__':
    app.run(debug=True)
