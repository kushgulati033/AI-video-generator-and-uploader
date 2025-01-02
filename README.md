# AI Video Generator and YouTube Uploader

An automated Python application that generates video content using AI, creates videos with text overlays, and uploads them to YouTube automatically.

## Features

- AI-powered content generation using OpenAI's GPT models
- Automated video creation with text overlays
- Direct YouTube uploading with proper authentication
- Comprehensive error handling and logging
- Automated cleanup of temporary files

## Prerequisites

Before running this application, make sure you have:

- Python 3.8 or higher installed
- FFmpeg installed on your system
- An OpenAI API key
- A Google Cloud Project with YouTube Data API enabled
- YouTube API credentials

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd ai-video-generator
```

2. Install required packages:
```bash
pip install moviepy google-auth-oauthlib google-auth google-api-python-client openai
```

3. Install FFmpeg (if not already installed):
- **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html)
- **MacOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

## Configuration

1. Create a copy of `config_example.json` and name it `config.json`:
```json
{
    "openai_key": "your_openai_api_key",
    "youtube_credentials_file": "path_to_your_youtube_credentials.json",
    "background_video_path": "path_to_your_background_video.mp4"
}
```

2. Set up YouTube API:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable YouTube Data API v3
   - Create OAuth 2.0 credentials
   - Download the client configuration file and save as `youtube_credentials.json`

3. Get OpenAI API key:
   - Go to [OpenAI API](https://platform.openai.com/api-keys)
   - Create a new API key
   - Add it to your config.json file

## Usage

Basic usage:

```python
from video_generator import AIVideoGenerator

# Initialize the generator
generator = AIVideoGenerator(
    openai_key='your_openai_api_key',
    youtube_credentials_file='path_to_your_credentials.json'
)

# Generate and upload a video
video_id = generator.generate_and_upload(
    prompt="Create a 1-minute educational video about space exploration",
    background_video_path="path_to_background.mp4",
    title="Space Exploration - AI Generated"
)
```

## Project Structure

```
ai-video-generator/
├── video_generator.py     # Main application code
├── config.json           # Configuration file
├── README.md            # This file
├── requirements.txt     # Python dependencies
└── logs/               # Log files directory
    └── video_generator.log
```

## Error Handling

The application includes comprehensive error handling and logging:
- All operations are logged to `video_generator.log`
- Errors are caught and logged with detailed information
- Failed operations are properly cleaned up

## Limitations

- Videos are initially uploaded as private for safety
- Background video must be provided
- Text overlay options are currently limited to basic styling
- API rate limits apply based on your API tier

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT API
- Google for YouTube Data API
- MoviePy contributors

## Support

For support, please:
1. Check the existing issues
2. Create a new issue with detailed information about your problem
3. Include relevant log files and configuration (without sensitive information)

## Security Notes

- Never commit API keys or credentials
- Always use environment variables or secure configuration management
- Review YouTube's content policies before automated uploading
