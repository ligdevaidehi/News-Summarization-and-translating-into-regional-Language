
# News Summarizer and Translator 📰

## Project Overview
The News Summarizer and Translator project aims to provide concise and accurate summaries of news articles, translating them into various regional languages to enhance accessibility and understanding for a broader audience. This project leverages natural language processing (NLP) and machine learning techniques to automate the summarization and translation processes.

## Features
- Extract full text from news articles.
- Generate concise summaries of news articles.
- Translate summaries into multiple regional languages, including Hindi, Marathi, Telugu, and Tamil.
- User-friendly interface for inputting URLs and selecting summary preferences.

## Technologies Used
- **Streamlit**: For building the web interface.
- **Requests**: For fetching web content.
- **BeautifulSoup**: For parsing HTML content.
- **NLTK**: For natural language processing tasks.
- **Googletrans**: For translating text into different languages.

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Steps
1. **Clone the repository**:

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data**:
   ```python
   import nltk
   nltk.download('punkt')
   ```

## Usage
1. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Interact with the app**:
   - Enter the URL of the news article you want to summarize.
   - Select the language you want the summary to be translated to.
   - Choose the desired length of the summary (Low, Medium, High).
   - Click the "Summarize" button to generate and view the translated summary.

## File Structure
- `app.py`: Main application script.
- `requirements.txt`: List of required Python packages.
- `README.md`: Project description and setup instructions.
