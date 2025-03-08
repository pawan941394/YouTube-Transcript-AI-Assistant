<div align="center">

# 📝 YouTube Transcript Extractor & Chat

<img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="Made with Python">
<img src="https://img.shields.io/badge/Streamlit-%23FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white" alt="Streamlit">
<img src="https://img.shields.io/badge/YouTube-%23FF0000.svg?style=flat&logo=YouTube&logoColor=white" alt="YouTube">
<a href="https://www.youtube.com/@Pawankumar-py4tk?sub_confirmation=1"><img src="https://img.shields.io/youtube/channel/subscribers/UC_k33KzNxQ3z3bGLZJBGUaA?style=social" alt="YouTube Channel Subscribers"></a>

<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHk5ZzdxeHZlamxxdnA0MnM1NzMydnY3MjRvNnQzbjRjZnlxcmJmaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPEqDGUULpEU0aQ/giphy.gif" width="400" alt="Animated Typing">
</p>

<p>A powerful tool to extract transcripts from any YouTube video and chat with the content using AI 💬</p>
<p>Created by <a href="https://www.youtube.com/@Pawankumar-py4tk">@Pawankumar-py4tk</a></p>

</div>

---

## ✨ Live Demo

Try the tool online: [Launch App](#) *(Add your deployment link when available)*

<p align="center">
  <img src="screenshots/maininterfaceimage.png" width="800" alt="App Demo">
  <br><i>👆 Main interface of YouTube Transcript Extractor</i>
</p>

## 🌟 Features

<table>
<tr>
<td>

- ✅ **Extract Transcripts**: Get the complete transcript from any YouTube video with just a URL
- ✅ **Multiple Languages**: Support for transcripts in different languages and auto-generated captions
- ✅ **AI Chat Interface**: Ask questions about the video content and get answers based on the transcript
- ✅ **Download Options**: Save transcripts as text files for offline use
- ✅ **User-Friendly Interface**: Clean Streamlit web interface for easy interaction

</td>
<td>

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXVreDJmZjI5a3JqcDZ0enpveXVrdmgxendzMnRrZm8zaHFrbXh3ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l46Cy1rHbQ92uuLXa/giphy.gif" width="240" alt="Transcription Animation">

</td>
</tr>
</table>

## 🚀 Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/youtube-transcript-extractor.git
cd youtube-transcript-extractor
```

2. **Install required packages**
```bash
pip install -r requirements.txt
```

3. **Run the application**

Command line version:
```bash
python youtube.py
```

Streamlit web interface:
```bash
streamlit run streamlit_app.py
```

## 💻 Screenshots

<div align="center">
<table>
  <tr>
    <td width="50%">
      <img src="screenshots/maininterfaceimage.png" alt="Main Interface" width="100%"/>
      <p align="center"><i>Main interface - Transcript extraction</i></p>
    </td>
    <td width="50%">
      <img src="screenshots/chatimag.png" alt="AI Chat Interface" width="100%"/>
      <p align="center"><i>AI Chat with transcript content</i></p>
    </td>
  </tr>
  <tr>
    <td colspan="2">
      <img src="screenshots/about.png" alt="About Section" width="100%"/>
      <p align="center"><i>About section with creator information</i></p>
    </td>
  </tr>
</table>
</div>

## 🤖 AI Chat Feature

<table>
<tr>
<td width="60%">
The AI chat feature uses an Ollama-hosted LLM to answer questions based on the video transcript. You can:

- 💡 Ask for summaries of the video content
- 🔍 Query specific information mentioned in the video
- 📚 Request explanations of concepts discussed in the transcript
- 🔄 Get key points and timestamps from long videos
</td>
<td width="40%">
<img src="screenshots/chatimag.png" width="100%" alt="Chat Feature Screenshot">
</td>
</tr>
</table>

## 🔧 Configuration

If you want to use a different LLM API, you can modify the following constants in `streamlit_app.py`:

```python
# Constants for Ollama API
OLLAMA_API_URL = "https://your-api-url.com/api/chat"
OLLAMA_MODEL = "your-model-name"
```

## 📁 Project Structure

```
youtube-transcript-extractor/
├── youtube.py               # Core functionality for transcript extraction
├── streamlit_app.py         # Streamlit web interface
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── screenshots/             # Application screenshots
│   ├── maininterfaceimage.png  # Main interface screenshot
│   ├── chatimag.png         # Chat interface screenshot
│   └── about.png            # About section screenshot
└── LICENSE                  # MIT License
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

<div align="center">
  <a href="https://www.youtube.com/@Pawankumar-py4tk">
    <img src="https://img.shields.io/badge/YouTube-Pawan_Kumar-red?style=for-the-badge&logo=youtube" alt="YouTube Channel">
  </a>
  <br>
  <a href="https://www.youtube.com/@Pawankumar-py4tk">
    <img src="https://img.shields.io/youtube/channel/subscribers/UC_k33KzNxQ3z3bGLZJBGUaA?style=social" alt="YouTube Subscribers">
  </a>
</div>

<table>
  <tr>
    <td width="150" align="center">
      <a href="https://www.youtube.com/@Pawankumar-py4tk">
        <img src="https://yt3.googleusercontent.com/ytc/APkrFKaauDQYCDaAqfuMkymABQhhE3ppW2Sa3NEjrQ=s176-c-k-c0x00ffffff-no-rj" width="100" style="border-radius:50%">
      </a>
    </td>
    <td>
      <h3><a href="https://www.youtube.com/@Pawankumar-py4tk">Pawan Kumar</a></h3>
      <p>I create Python tutorials and tools to help make programming and AI more accessible. Follow me for more useful content!</p>
      <p>
        <a href="https://www.youtube.com/@Pawankumar-py4tk?sub_confirmation=1">
          <img src="https://img.shields.io/badge/Subscribe-red?style=for-the-badge&logo=youtube">
        </a>
      </p>
    </td>
  </tr>
</table>

## 🙏 Acknowledgements

- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) for making transcript extraction possible
- [Streamlit](https://streamlit.io/) for the web interface framework
- [Ollama](https://ollama.com/) for hosting the LLM service

## ⭐ Support

If you find this tool useful, please consider:
- 🌟 Giving it a star on GitHub
- 📺 [Subscribing to my YouTube channel](https://www.youtube.com/@Pawankumar-py4tk?sub_confirmation=1) for more Python tutorials
- 🔀 Contributing to the project with improvements and bug fixes

---

<div align="center">
  <a href="https://www.youtube.com/@Pawankumar-py4tk?sub_confirmation=1">
    <img src="https://img.shields.io/badge/Subscribe%20to%20@Pawankumar--py4tk-red?style=for-the-badge&logo=youtube&logoColor=white" alt="Subscribe">
  </a>
</div>

<p align="center">
  <i>This tool uses the YouTube Transcript API and is not affiliated with YouTube or Google.<br>
  Use responsibly and in accordance with YouTube's terms of service.</i>
</p>
