
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import os
from dotenv import load_dotenv
import json
from tqdm import tqdm
import time
import random
from datetime import datetime

load_dotenv()

# Set up YouTube API client
youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

def get_channel_upload_playlist_id(channel_id):
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )
    response = request.execute()
    return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

def get_all_video_ids(playlist_id):
    video_ids = []
    next_page_token = None
    
    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        
        for item in response['items']:
            video_ids.append(item['snippet']['resourceId']['videoId'])
        
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    return video_ids

def get_video_details(video_id):
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    response = request.execute()
    snippet = response['items'][0]['snippet']
    statistics = response['items'][0]['statistics']
    
    # Get the highest resolution thumbnail available
    thumbnails = snippet['thumbnails']
    thumbnail_url = thumbnails.get('maxres', thumbnails.get('standard', thumbnails.get('high', thumbnails.get('medium', thumbnails['default']))))['url']
    
    return snippet, statistics, thumbnail_url

def get_video_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to get the manually created English transcript first
        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
        except:
            # If no manually created English transcript, try auto-generated
            transcript = transcript_list.find_generated_transcript(['en'])
        
        full_transcript = transcript.fetch()
        return {
            'text': ' '.join([entry['text'] for entry in full_transcript]),
            'language': transcript.language_code
        }
    except Exception as e:
        return {
            'text': None,
            'language': None,
            'error': str(e)
        }

def main():
    channel_id = 'UCe0TLA0EsQbE-MjuHXevj2A'  # AthleanX channel ID
    
    # Get the upload playlist ID
    upload_playlist_id = get_channel_upload_playlist_id(channel_id)
    
    # Get all video IDs
    all_video_ids = get_all_video_ids(upload_playlist_id)
    
    print(f"Total videos found: {len(all_video_ids)}")
    
    # Create data directory if it doesn't exist
    os.makedirs('data/raw', exist_ok=True)
    
    videos_with_transcript = 0
    videos_without_transcript = 0
    english_videos = 0

    try:
        for video_id in tqdm(all_video_ids, desc="Processing videos"):
            video_details, video_statistics, thumbnail_url = get_video_details(video_id)
            transcript_data = get_video_transcript(video_id)
            
            # Skip non-English videos
            if transcript_data['language'] != 'en':
                continue
            
            english_videos += 1
            
            # Convert the publishedAt date to a more readable format
            published_at = datetime.strptime(video_details['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            formatted_date = published_at.strftime("%Y-%m-%d %H:%M:%S")
            
            video_data = {
                'id': video_id,
                'title': video_details['title'],
                'description': video_details['description'],
                'upload_date': formatted_date,
                'view_count': video_statistics['viewCount'],
                'like_count': video_statistics.get('likeCount', 'N/A'),
                'comment_count': video_statistics.get('commentCount', 'N/A'),
                'thumbnail_url': thumbnail_url,
                'transcript': transcript_data['text'],
                'transcript_language': transcript_data['language'],
                'transcript_error': transcript_data.get('error')
            }
            
            with open(f'data/raw/{video_id}.json', 'w', encoding='utf-8') as f:
                json.dump(video_data, f, ensure_ascii=False, indent=4)
            
            if transcript_data['text']:
                videos_with_transcript += 1
            else:
                videos_without_transcript += 1
            
            # Print progress
            print(f"\rProcessed: {english_videos}/{len(all_video_ids)} | "
                  f"English videos: {english_videos} | "
                  f"With transcript: {videos_with_transcript} | "
                  f"Without transcript: {videos_without_transcript}", end="")
            
            # Add a small delay between requests to avoid rate limiting
            time.sleep(random.uniform(1, 3))
    
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user. Saving progress...")
    
    finally:
        print("\n\nFinal Statistics:")
        print(f"Total English videos processed: {english_videos}")
        print(f"Videos with transcript: {videos_with_transcript}")
        print(f"Videos without transcript: {videos_without_transcript}")

if __name__ == '__main__':
    main()
    
    # # from googleapiclient.discovery import build
# # from youtube_transcript_api import YouTubeTranscriptApi
# # import os
# # from dotenv import load_dotenv
# # import json
# # from tqdm import tqdm

# # load_dotenv()

# # # Set up YouTube API client
# # youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

# # def get_channel_videos(channel_id):
# #     videos = []
# #     request = youtube.search().list(
# #         part='snippet',
# #         channelId=channel_id,
# #         maxResults=50,
# #         type='video'
# #     )
# #     while request:
# #         response = request.execute()
# #         videos.extend(response['items'])
# #         request = youtube.search().list_next(request, response)
# #     return videos

# # def get_video_transcript(video_id):
# #     try:
# #         transcript = YouTubeTranscriptApi.get_transcript(video_id)
# #         return ' '.join([entry['text'] for entry in transcript])
# #     except:
# #         return None

# # def main():
# #     channel_id = 'UCe0TLA0EsQbE-MjuHXevj2A'
# #     videos = get_channel_videos(channel_id)
    
# #     # Create data directory if it doesn't exist
# #     os.makedirs('data/raw', exist_ok=True)
    
# #     for video in tqdm(videos, desc="Processing videos"):
# #         video_id = video['id']['videoId']
# #         video_data = {
# #             'id': video_id,
# #             'title': video['snippet']['title'],
# #             'description': video['snippet']['description'],
# #             'transcript': get_video_transcript(video_id)
# #         }
        
# #         with open(f'data/raw/{video_id}.json', 'w', encoding='utf-8') as f:
# #             json.dump(video_data, f, ensure_ascii=False, indent=4)

# # if __name__ == '__main__':
# #     main()

# from googleapiclient.discovery import build
# from youtube_transcript_api import YouTubeTranscriptApi
# import os
# from dotenv import load_dotenv
# import json
# from tqdm import tqdm

# load_dotenv()

# # Set up YouTube API client
# youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

# def get_channel_upload_playlist_id(channel_id):
#     request = youtube.channels().list(
#         part="contentDetails",
#         id=channel_id
#     )
#     response = request.execute()
#     return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# def get_all_video_ids(playlist_id):
#     video_ids = []
#     next_page_token = None
    
#     while True:
#         request = youtube.playlistItems().list(
#             part="snippet",
#             playlistId=playlist_id,
#             maxResults=50,
#             pageToken=next_page_token
#         )
#         response = request.execute()
        
#         for item in response['items']:
#             video_ids.append(item['snippet']['resourceId']['videoId'])
        
#         next_page_token = response.get('nextPageToken')
#         if not next_page_token:
#             break
    
#     return video_ids

# def get_video_details(video_id):
#     request = youtube.videos().list(
#         part="snippet",
#         id=video_id
#     )
#     response = request.execute()
#     return response['items'][0]['snippet']

# def get_video_transcript(video_id):
#     try:
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)
#         return ' '.join([entry['text'] for entry in transcript])
#     except:
#         return None

# def main():
#     channel_id = 'UCe0TLA0EsQbE-MjuHXevj2A'  # AthleanX channel ID
    
#     # Get the upload playlist ID
#     upload_playlist_id = get_channel_upload_playlist_id(channel_id)
    
#     # Get all video IDs
#     all_video_ids = get_all_video_ids(upload_playlist_id)
    
#     print(f"Total videos found: {len(all_video_ids)}")
    
#     # Create data directory if it doesn't exist
#     os.makedirs('data/raw', exist_ok=True)
    
#     for video_id in tqdm(all_video_ids, desc="Processing videos"):
#         video_details = get_video_details(video_id)
#         video_data = {
#             'id': video_id,
#             'title': video_details['title'],
#             'description': video_details['description'],
#             'transcript': get_video_transcript(video_id)
#         }
        
#         with open(f'data/raw/{video_id}.json', 'w', encoding='utf-8') as f:
#             json.dump(video_data, f, ensure_ascii=False, indent=4)

# if __name__ == '__main__':
#     main()
