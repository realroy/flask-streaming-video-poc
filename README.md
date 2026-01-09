# Flask Video Streaming POC

A Flask application that streams avatar videos based on state, deployable on Vercel.

## Features

- Video streaming API endpoint: `GET /api/v1/avatar?state=<nodding|speaking>`
- Simple web interface with video player and state controls
- Vercel-ready deployment configuration

## Project Structure

```
flask-video-streaming-poc/
├── api/
│   └── index.py          # Flask application
├── static/
│   └── videos/
│       ├── avatar-nodding.mp4   # Add your video file
│       └── avatar-speaking.mp4  # Add your video file
├── templates/
│   └── index.html        # Home page template
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies (for Vercel)
├── pyproject.toml        # Project metadata
└── uv.lock               # uv lockfile
```

## Setup

### 1. Add Video Files

Place your MP4 video files in the `static/videos/` directory:
- `avatar-nodding.mp4`
- `avatar-speaking.mp4`

### 2. Install Dependencies

```bash
uv sync
```

### 3. Run Locally

```bash
uv run flask --app api/index run --debug
```

Then open http://localhost:5000 in your browser.

## API Endpoint

### GET /api/v1/avatar

Streams an avatar video based on the specified state.

**Query Parameters:**
- `state` (required): Either `nodding` or `speaking`

**Responses:**
- `200 OK`: Returns MP4 video stream
- `400 Bad Request`: Invalid or missing state parameter
- `404 Not Found`: Video file not found

**Example:**
```
GET /api/v1/avatar?state=nodding
```

## Deploy to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in the project directory
3. Follow the prompts to deploy

Note: Make sure your video files are added before deploying.
