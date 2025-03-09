import streamlit as st
import pandas as pd
from youtube import extract_video_id, get_best_transcript, save_transcript_to_file
import base64
import os
import time
import requests
import json
import random

# Set page config
st.set_page_config(
    page_title="YouTube Transcript Extractor by @Pawankumar-py4tk",
    page_icon="🤖",
    layout="wide"
)

# Add custom CSS for AI styling
st.markdown("""
<style>
    /* AI Chat styling */
    .ai-badge {
        background-color: black;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 0.5rem;
        font-size: 0.8rem;
        font-weight: bold;
        margin-right: 0.5rem;
    }
    
    .ai-container {
        border-left: 4px solid #8B44FF;
        padding-left: 1rem;
        margin: 1rem 0;
    }
    
    .ai-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .ai-thinking {
        color: #8B44FF;
        font-style: italic;
    }
    
    /* Pulsating AI effect */
    .ai-pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* AI Tool Card */
    .ai-tool-card {
        border: 1px solid #f0f0f5;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        background: black;
    }
    
    .ai-tool-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Channel branding */
    .channel-banner {
        background: linear-gradient(90deg, #FF0000 0%, #FF5500 100%);
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Constants for Ollama API
OLLAMA_API_URL = "{your ollama url}/api/chat"
OLLAMA_MODEL = "llama3.2:latest"

# Channel information
CHANNEL_NAME = "Pawan Kumar"
CHANNEL_USERNAME = "@Pawankumar-py4tk"
CHANNEL_URL = "https://www.youtube.com/@Pawankumar-py4tk"
CHANNEL_DESCRIPTION = "Learn Python and AI tools with practical examples and tutorials."

# GenAI Icons for rotating display
AI_ICONS = ["🤖", "🧠", "💬", "🔮", "📊", "🔍", "⚙️", "💻", "🧩", "🌐", "🚀", "📝"]

def get_ai_icon():
    """Get a random AI-related emoji"""
    return random.choice(AI_ICONS)

def display_header():
    """Display branded header with channel information"""
    # Channel banner with AI icon

    
    col1, col2 = st.columns([1, 3])
    
    with col2:
        st.title("📝 YouTube Transcript AI Assistant")
        st.markdown(f"### Created by [{CHANNEL_NAME} ({CHANNEL_USERNAME})]({CHANNEL_URL})")

def display_ai_features():
    """Display AI features with nice icons"""
    st.markdown("## 🧠 AI-Powered Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="ai-tool-card">
            <h3>🔍 Transcript Extraction</h3>
            <p>AI-powered extraction of YouTube transcripts with support for multiple languages.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="ai-tool-card">
            <h3>💬 Interactive Chat</h3>
            <p>Chat with video content using latest LLM technology to understand key points.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="ai-tool-card">
            <h3>📊 Content Analysis</h3>
            <p>Get summaries, insights, and analyze video content efficiently.</p>
        </div>
        """, unsafe_allow_html=True)

def display_video_info(video_id):
    """Display YouTube video thumbnail and embed"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg", 
                 caption="Video Thumbnail", 
                 use_container_width =True)
    
    with col2:
        st.write("Video Preview:")
        st.components.v1.iframe(
            src=f"https://www.youtube.com/embed/{video_id}",
            width=400, 
            height=225,
            scrolling=False
        )

def query_ollama(prompt, transcript, history=None):
    """Query the Ollama API with the transcript as context"""
    if history is None:
        history = []
    
    # Ensure transcript is properly formatted and not empty
    if not transcript or transcript.startswith("Error"):
        return "I don't have access to the transcript. Please extract a valid transcript first."
    
    # Simplify the approach: combine prompt and transcript in a single query
    # This avoids relying on the model to remember the transcript across turns
    current_query = f"""I want you to answer this question based only on the YouTube transcript provided below.
    
Question: {prompt}

Transcript:
{transcript}
"""

    try:
        # Create payload with minimal history
        messages = []
        
        # Only include system message and recent history (limit to 2 previous exchanges)
        messages.append({
            "role": "system", 
            "content": "You are an assistant that answers questions about YouTube video transcripts. Base your answers only on the information in the transcript provided in each query."
        })
        
        # Add limited conversation history if it exists
        recent_history = history[-4:] if len(history) > 4 else history
        for msg in recent_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add the current query with embedded transcript
        messages.append({"role": "user", "content": current_query})
        
        # For debugging
        st.session_state.last_api_request = {
            "model": OLLAMA_MODEL,
            "messages_count": len(messages),
            "current_query_preview": current_query[:100] + "..."
        }
        
        payload = {
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            # Add parameters to control response
            "temperature": 0.1,  # Lower temperature for more focused responses
            "max_tokens": 800    # Limit response length
        }
        
        response = requests.post(
            OLLAMA_API_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            response_content = result.get("message", {}).get("content", "")
            
            # Check for problematic responses
            problematic_phrases = [
                "provide the transcript", 
                "don't see the transcript",
                "didn't share a transcript",
                "need the transcript",
                "share the transcript"
            ]
            
            if any(phrase in response_content.lower() for phrase in problematic_phrases):
                return "I'm having trouble analyzing the transcript. Let me try a different approach to answer your question about the video content."
            
            return response_content
        else:
            # Log the error response
            st.session_state.last_api_error = f"Status code: {response.status_code}, Response: {response.text[:500]}"
            return f"Error: API returned status code {response.status_code}. Please try again or ask a different question."
    
    except Exception as e:
        st.session_state.last_api_error = str(e)
        return f"Error communicating with Ollama API. Please try again. Error: {str(e)}"

def chat_interface(transcript):
    """Display chat interface for interacting with the transcript"""
    st.markdown(f"""
    <div class="ai-header">
        <span class="ai-badge">AI ASSISTANT</span>
        <span>LLM-powered transcript analysis</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("💬 Chat with the Transcript")
    st.write("Ask questions about the video content and get answers based on the transcript.")
    
    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Add buttons for chat controls with AI icons
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col2:
        if st.button("🧹 Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    with col3:
        if st.button("🧠 Quick Analysis"):
            # Add an AI analysis request to the chat
            with st.spinner("AI is analyzing the content..."):
                quick_analysis_prompt = "Give me a quick summary and the main topics of this video based on the transcript."
                analysis_response = query_ollama(quick_analysis_prompt, transcript, [])
                
                # Add to chat history
                st.session_state.chat_history.append({"role": "user", "content": quick_analysis_prompt})
                st.session_state.chat_history.append({"role": "assistant", "content": analysis_response})
                st.rerun()
    
    # Display chat messages with AI styling
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message["content"])
    
    # Chat input with AI icon
    user_query = st.chat_input("🔍 Ask AI about the video content...")
    
    if user_query:
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.write(user_query)
        
        # Add to history
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        # Get AI response with loading indicator
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🧠 AI is thinking..."):
                response = query_ollama(
                    user_query, 
                    transcript, 
                    st.session_state.chat_history[:-1]  # Exclude the current message
                )
            st.write(response)
        
        # Add to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})

def display_footer():
    """Display footer with channel information and links"""
    st.divider()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("### About")
        st.write(f"This tool was created by [{CHANNEL_NAME}]({CHANNEL_URL}) to help you extract and interact with YouTube video transcripts.")
        st.write(CHANNEL_DESCRIPTION)
    
    with col2:
        st.markdown("### Subscribe")
        st.markdown(f"""
        <a href="{CHANNEL_URL}?sub_confirmation=1" target="_blank">
            <img src="https://img.shields.io/youtube/channel/subscribers/UC_k33KzNxQ3z3bGLZJBGUaA?style=social" alt="Subscribe to {CHANNEL_NAME}">
        </a>
        """, unsafe_allow_html=True)
        st.write("Subscribe to my channel for more Python and AI tutorials!")
    
    with col3:
        st.markdown("### Other Tools")
        st.write("Check out my other Python tools and tutorials:")
        st.markdown(f"[Visit My Channel]({CHANNEL_URL})")
    
    # Copyright notice
    st.caption(f"© {time.strftime('%Y')} {CHANNEL_NAME} | YouTube Transcript Extractor & Chat | Powered by youtube-transcript-api and Ollama LLM")

def main():
    # Display branded header
    display_header()
    
    st.markdown(f"""
    <div class="ai-container">
        <p>{get_ai_icon()} Get the complete transcript of any YouTube video and chat with the content using AI.
        This tool leverages advanced language models to help you interact with video content.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add AI features section
    display_ai_features()
    
    # Add a link to the creator's channel
    st.markdown(f"""
    <div style="background-color:black; padding:10px; border-radius:5px; margin-bottom:10px;">
        <small>❤️ If you find this AI tool useful, please consider <a href="{CHANNEL_URL}?sub_confirmation=1" target="_blank">subscribing to my YouTube channel</a> for more Python and AI tools.</small>
    </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs(["🔍 Extract Transcript", "🤖 AI Chat", "ℹ️ About"])
    
    with tabs[0]:
        # Input for YouTube URL
        st.markdown("<h3>🎬 Enter YouTube Video URL</h3>", unsafe_allow_html=True)
        youtube_url = st.text_input("", 
                                  placeholder="https://www.youtube.com/watch?v=...",
                                  key="url_input")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        extract_btn = col1.button("🔍 Extract Transcript", type="primary")
        demo_btn = col2.button("🎮 Try Demo Video")
        
        # Add a button to visit your channel
        if col3.button("📺 Visit My Channel"):
            st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{CHANNEL_URL}\'" />', unsafe_allow_html=True)
        
        # Use session state to store transcript
        if 'transcript' not in st.session_state:
            st.session_state.transcript = ""
            st.session_state.video_id = ""
        
        # Demo video - use one from your channel if available
        if demo_btn:
            youtube_url = "https://youtu.be/5WtVOYh15Nk?si=FzGqfx_U3GIXbP9h"  # You can replace with a video from your channel
            st.session_state.video_id = extract_video_id(youtube_url)
            
            with st.spinner("Extracting transcript..."):
                st.session_state.transcript = get_best_transcript(youtube_url)
        
        # Extract transcript when button is clicked
        if extract_btn and youtube_url:
            video_id = extract_video_id(youtube_url)
            
            if not video_id:
                st.error("Invalid YouTube URL. Please check the URL and try again.")
            else:
                st.session_state.video_id = video_id
                with st.spinner("Extracting transcript..."):
                    st.session_state.transcript = get_best_transcript(youtube_url)
                    time.sleep(0.5)  # Small delay for better UX
                # Reset chat history when new transcript is loaded
                if "chat_history" in st.session_state:
                    st.session_state.chat_history = []
        
        # Display video and transcript if available
        if st.session_state.video_id:
            st.divider()
            display_video_info(st.session_state.video_id)
            
            st.divider()
            st.subheader("Transcript")
            
            if st.session_state.transcript.startswith("Error"):
                st.error(st.session_state.transcript)
            else:
                # Add word count
                word_count = len(st.session_state.transcript.split())
                st.write(f"**Word count:** {word_count}")
                
                # Display transcript in expandable text area
                with st.expander("View Full Transcript", expanded=True):
                    st.text_area("", st.session_state.transcript, height=300)
                
                # Save to local file option
                if st.button("Save to local file"):
                    try:
                        filepath = save_transcript_to_file(st.session_state.transcript, st.session_state.video_id)
                        st.success(f"Transcript saved to: {filepath}")
                    except Exception as e:
                        st.error(f"Failed to save file: {str(e)}")
    
    with tabs[1]:
        if not st.session_state.transcript or st.session_state.transcript.startswith("Error"):
            st.info("🔍 Please extract a transcript first to chat with the AI.")
            
            # Add a promotional message with AI styling
            st.markdown(f"""
            <div class="ai-container">
                <div class="ai-header">
                    <span class="ai-badge">TIP</span>
                </div>
                <p>While you're here, check out my <a href="{CHANNEL_URL}" target="_blank">YouTube channel</a> for Python and AI tutorials!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            chat_interface(st.session_state.transcript)
    
    with tabs[2]:
        st.header(f"About {CHANNEL_NAME}")
        st.write("""
        This tool was created to help YouTube viewers extract and interact with video transcripts.
        It's particularly useful for:
        
        - Students who want to study video content
        - Researchers collecting information from videos
        - Content creators analyzing other videos
        - Anyone who prefers reading over watching
        """)
        
        st.subheader("How it works")
        st.write("""
        1. Enter a YouTube URL in the "Extract Transcript" tab
        2. The tool fetches the transcript using YouTube's API
        3. You can view, download, or chat with the transcript content
        4. The AI chat functionality helps you understand video content through Q&A
        """)
        
        st.subheader("About the Creator")
        st.write(f"""
        [{CHANNEL_NAME}]({CHANNEL_URL}) creates Python tutorials and tools to help make programming and AI more accessible.
        Subscribe to the channel for more useful tools and tutorials!
        """)
        
        # Subscribe button
        st.markdown(f"""
        <a href="{CHANNEL_URL}?sub_confirmation=1" target="_blank">
            <button style="background-color:#FF0000; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;">
                Subscribe to {CHANNEL_USERNAME}
            </button>
        </a>
        """, unsafe_allow_html=True)
    
    # Display footer with branding
    display_footer()

if __name__ == "__main__":
    main()
