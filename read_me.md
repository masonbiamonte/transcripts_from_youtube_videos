# Italian Language Transcript Generator from YouTube Video URLs *(Generatore automatico di trascrizioni in lingua italiana dagli URL dei video di YouTube)*

This project streamlines the process of downloading and saving Italian language transcripts, along with their English translations, using the [YouTubeTranscriptApi](https://pypi.org/project/youtube-transcript-api/) in `.docx` format. No major conceptual contributions were made in the writing of this code (as of the June 19, 2021 version @ 6:07 PM CDT). That is, this code implements the API, cleans up the text data and saves it Word documents. The idea behind the project is to create a tool for language learners. 

## Installation

To install all dependencies, simply navigate to the local directory in which this project is saved and run

```bash
pip install -r requirements.txt
```

## Usage

Simply run `python3 gen_transcript_from_URL.py`. The terminal will prompt you for a YouTube URL. Either copy and paste or type in the URL by hand and press enter. If a transcript exists, the program will download both the Italian original language and English translation texts and save them nicely into Word documents, whether or not the text is structured/punctuated, inside folders named with the corresponding video title.

## Next Steps
By unstructured/unpunctuated text it is meant that the transcript comes as a single string with no capitalization, commas or periods. Thus, it would be desirable to use a trained NLP model to take unstructured text as input and reconstruct sentence boundaries. This is a very non-trivial instance of sentence tokenization. An obvious approach would be to find a large corpus of punctuated Italian sentences and remove the punctuation to create a training set. Another improvement would to use language-translation NLP to construct a combined Italian+English transcript for unstructured instances. 
