import re
import os
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def extract_video_id(youtube_url):
    """Extract the video ID from a YouTube URL."""
    # Regular expression patterns for different YouTube URL formats
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',  # Standard and shortened URLs
        r'(?:embed\/)([0-9A-Za-z_-]{11})',   # Embed URLs
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'  # youtu.be URLs
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    
    return None

def get_available_transcripts(video_id):
    """Get list of available transcript languages for a video."""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        available_languages = []
        
        for transcript in transcript_list:
            language_code = transcript.language_code
            language_name = transcript.language
            available_languages.append((language_code, language_name))
            
        return available_languages
    except Exception:
        return []

def get_best_transcript(youtube_url):
    """Try multiple approaches to get the best available transcript."""
    video_id = extract_video_id(youtube_url)
    
    if not video_id:
        return "Error: Could not extract video ID from the URL."
    
    try:
        # Try default transcript first
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return format_transcript(transcript_list)
    except (TranscriptsDisabled, NoTranscriptFound):
        # Try to get available languages
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # First try English if available
            try:
                english_transcript = transcript_list.find_transcript(['en'])
                transcript_list = english_transcript.fetch()
                return format_transcript(transcript_list)
            except:
                pass
            
            # If English not available, try auto-generated
            try:
                auto_transcript = transcript_list.find_generated_transcript(['en', 'en-US'])
                transcript_list = auto_transcript.fetch()
                return format_transcript(transcript_list)
            except:
                pass
            
            # As last resort, use the first available transcript
            available = list(transcript_list)
            if available:
                transcript_list = available[0].fetch()
                return format_transcript(transcript_list)
            
            return "Error: No usable transcripts found for this video."
        except Exception as e:
            return f"Error: No transcripts available. {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def format_transcript(transcript_list):
    """Format transcript for better readability."""
    transcript_text = ""
    for segment in transcript_list:
        transcript_text += segment['text'] + " "
    return transcript_text

def save_transcript_to_file(transcript, video_id):
    """Save transcript to a text file."""
    filename = f"{video_id}_transcript.txt"
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(transcript)
    
    return filepath

def main():
    print("YouTube Video Transcript Extractor")
    print("==================================")
    print("This tool will try multiple methods to get transcripts, including auto-generated captions")
    
    while True:
        youtube_url = input("\nEnter YouTube video URL (or 'q' to quit): ")
        
        if youtube_url.lower() == 'q':
            break
            
        transcript = get_best_transcript(youtube_url)
        
        print("\n--- TRANSCRIPT ---")
        print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
        print("------------------\n")
        
        if not transcript.startswith("Error"):
            save_option = input("Save transcript to file? (y/n): ").lower()
            if save_option == 'y':
                video_id = extract_video_id(youtube_url)
                filepath = save_transcript_to_file(transcript, video_id)
                print(f"Transcript saved to: {filepath}")

if __name__ == "__main__":
    main()
