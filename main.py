import os

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import openai
import json
from datetime import datetime
import logging


class AIVideoGenerator:
    def __init__(self, openai_key, youtube_credentials_file):
        """
        Initialize the video generator with necessary API keys and credentials
        """
        self.openai_key = openai_key
        self.youtube_credentials_file = youtube_credentials_file
        self.youtube = None
        self.setup_logging()

    def setup_logging(self):
        """Configure logging for the application"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='video_generator.log'
        )

    def authenticate_youtube(self):
        """
        Authenticate with YouTube API
        """
        try:
            SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
            flow = InstalledAppFlow.from_client_secrets_file(
                self.youtube_credentials_file, SCOPES)
            credentials = flow.run_local_server(port=0)
            self.youtube = build('youtube', 'v3', credentials=credentials)
            logging.info("YouTube authentication successful")
        except Exception as e:
            logging.error(f"YouTube authentication failed: {str(e)}")
            raise

    def generate_content(self, prompt):
        """
        Generate video content using OpenAI API
        """
        try:
            openai.api_key = self.openai_key
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a video script writer."},
                    {"role": "user", "content": prompt}
                ]
            )
            script = response.choices[0].message.content
            logging.info("Content generation successful")
            return script
        except Exception as e:
            logging.error(f"Content generation failed: {str(e)}")
            raise

    def create_video(self, script, background_video_path, output_path):
        """
        Create video with text overlay
        """
        try:
            # Load background video
            background = VideoFileClip(background_video_path)

            # Create text clip
            text_clip = TextClip(
                script,
                fontsize=70,
                color='white',
                size=background.size,
                method='caption'
            )
            text_clip = text_clip.set_duration(background.duration)

            # Composite video
            final_clip = CompositeVideoClip([background, text_clip])

            # Write output
            final_clip.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac'
            )

            # Clean up
            background.close()
            text_clip.close()
            final_clip.close()

            logging.info(f"Video created successfully: {output_path}")
            return output_path
        except Exception as e:
            logging.error(f"Video creation failed: {str(e)}")
            raise

    def upload_to_youtube(self, video_path, title, description, tags=None):
        """
        Upload video to YouTube
        """
        try:
            if not self.youtube:
                self.authenticate_youtube()

            tags = tags or []
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags,
                    'categoryId': '22'  # Entertainment category
                },
                'status': {
                    'privacyStatus': 'private',  # Start as private for safety
                    'selfDeclaredMadeForKids': False
                }
            }

            media = MediaFileUpload(
                video_path,
                chunksize=1024 * 1024,
                resumable=True
            )

            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )

            response = request.execute()
            video_id = response['id']
            logging.info(f"Video uploaded successfully. Video ID: {video_id}")
            return video_id
        except Exception as e:
            logging.error(f"Video upload failed: {str(e)}")
            raise

    def generate_and_upload(self, prompt, background_video_path, title=None):
        """
        Complete pipeline to generate and upload a video
        """
        try:
            # Generate content
            script = self.generate_content(prompt)

            # Create output path
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f'output_video_{timestamp}.mp4'

            # Create video
            video_path = self.create_video(script, background_video_path, output_path)

            # Generate title if not provided
            if not title:
                title = f"AI Generated Video - {timestamp}"

            # Upload to YouTube
            video_id = self.upload_to_youtube(
                video_path,
                title=title,
                description=f"AI generated video based on: {prompt}",
                tags=['AI Generated', 'Automated Content']
            )

            # Clean up
            os.remove(output_path)

            return video_id
        except Exception as e:
            logging.error(f"Pipeline failed: {str(e)}")
            raise


def main():
    # Configuration
    config = {
        'openai_key': 'your_openai_api_key',
        'youtube_credentials_file': 'path_to_your_youtube_credentials.json',
        'background_video_path': 'path_to_your_background_video.mp4'
    }

    # Initialize generator
    generator = AIVideoGenerator(
        config['openai_key'],
        config['youtube_credentials_file']
    )

    # Example prompt
    prompt = "Create a 1-minute educational video about space exploration"

    try:
        # Generate and upload video
        video_id = generator.generate_and_upload(
            prompt=prompt,
            background_video_path=config['background_video_path']
        )
        print(f"Video uploaded successfully! Video ID: {video_id}")
    except Exception as e:
        print(f"Error in pipeline: {str(e)}")


if __name__ == "__main__":
    main()
