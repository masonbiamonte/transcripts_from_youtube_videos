from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
from youtube_transcript_api import YouTubeTranscriptApi

import funcs
import os


"""

this code produces Italian, English and Italian+English transcripts
of Italian language YouTube videos directly from their URLs

some YouTube transcripts are auto-generated

these auto-generated transcripts consist of a single string of text
without any sentence delimiters or other punctuation

this identifies an immediate application of natural language processing (NLP):
sentence tokenization of error-ridden auto-generated YouTube transcripts

the above feature allows for a more complete automation of transcripts


"""

"""

example videos #1-5 are from the Nova Lectio channel:
https://www.youtube.com/channel/UCRCWJCFoZUvkkWzIqzfBy6g

example video #1: com'è crollata la nazione più ricca del sud america
video_url = 'https://www.youtube.com/watch?v=ouIMOJsCADY'
video_id = video_url.split("v=")[-1]

example video #2: è davvero la colpa del colonialismo se l'africa è un fallimento
video_url = 'https://www.youtube.com/watch?v=xAJEyMWVVnw'
video_id = video_url.split("v=")[-1]

example video #3: come la cina è diventata una potenza mondiale
video_url = 'https://www.youtube.com/watch?v=n5vIhOA60TM'
video_id = video_url.split("v=")[-1]

example video #4: il business infernale delle miniere di coltan in congo
video_url = 'https://www.youtube.com/watch?v=x-6f2OdXakI'
video_id = video_url.split("v=")[-1]

example video #5: come scappare il paese più blindato nel mondo
(structured example)
video_url = 'https://www.youtube.com/watch?v=V_QjLQaXbqk'
video_id = video_url.split("v=")[-1]

example video #6: alessandro barbero - la grande battaglia: gettysburg, 1863, Storia & Cultura
(unstructured example)
video_url = 'https://www.youtube.com/watch?v=y4HYjEZq21w'
video_id = video_url.split("v=")[-1]

example video #7: come fare la pasta cacio e pepe - ricetta dolci e cucina - tutorial
(no transcript example)
video_url = 'https://www.youtube.com/watch?v=s9Kd-0FiICw'
video_id = video_url.split("v=")[-1]

"""

# user input URL
video_url = input('YouTube video URL: ')
video_id = video_url.split("v=")[-1]
video_title = funcs.get_video_title(video_url)

# fetch Italian language transcript if it exists
transcript = False
try: 

	raw_it_script = YouTubeTranscriptApi.get_transcript(video_id, languages=['it'])
	transcript = True
	print('Collecting transcript...')

except:
	print('No transcript available for this URL. Please try another.')

if transcript:

	it_script_str = funcs.clean_script([phrase['text'] for phrase in raw_it_script])
	it_sentences = it_script_str.split("\n\n")
	num_it_sentences = len(it_sentences)

	# translate transcript to English and store as array of strings
	script_list = YouTubeTranscriptApi.list_transcripts(video_id)
	raw_en_script = script_list.find_transcript(['it']).translate('en').fetch()
	en_script_str = funcs.clean_script([phrase['text'] for phrase in raw_en_script])
	en_sentences = en_script_str.split("\n\n")

	# handle common English abbreviations with periods to avoid
	# false sentence creation when separating by the period char
	en_abbrevs = ['St.', 'Mr.', 'Mrs.', 'Dr.', ]

	for sentence in en_sentences:
		for abbrev in en_abbrevs:
			if abbrev in sentence:
				idx = en_sentences.index(sentence)
				en_sentences[idx] = sentence + ' ' + en_sentences[idx+1]
				en_sentences.remove(en_sentences[idx+1])

	en_script_str = '\n\n'.join(en_sentences)

	lang_strs = ['(italiano)', '(english)', '(italiano+english)']
	txt_filenames = funcs.get_txt_fnames(video_title, lang_strs)
	pdf_filenames = funcs.txt_to_other(txt_filenames, '.pdf')
	doc_filenames = funcs.txt_to_other(txt_filenames, '.docx')

	# print italian sentences on top of english sentences
	# and print a line between such pairs
	combo_script_str = str()
	script_strs = [it_script_str, en_script_str, combo_script_str]

	# form combined italian+english transcript string
	# and save all three transcripts as Word documents
	# in the case of a structured YouTube transcript
	if num_it_sentences > 1:

		print('Processing structured/punctuated transcript...')

		for i in range(len(it_sentences)):
		    combo_script_str += it_sentences[i] + "\n" + en_sentences[i] + "\n\n"

		funcs.scripts_to_doc(script_strs, doc_filenames)

	# otherwise, YouTube transcript comes as a single
	# string and needs to be processed differently than above
	elif num_it_sentences == 1:

		print('Processing unstructured/unpunctuated transcript...')

		# perform extra string processing on auto-generated
		# transcripts that are not partitioned into sentences
		char_line_lim = 80

		it_lines = funcs.script_to_lines(it_script_str, char_line_lim)
		en_lines = funcs.script_to_lines(en_script_str, char_line_lim)
		all_lines = [it_lines, en_lines]

		script_strs = list()
		curr_line = str()

		for lines in all_lines:

			lines_out = list()
			for i in range(len(lines)):
				if i%2 == 0:
					lines_out += lines[i] + '\n'
				else:
					lines_out += lines[i] + '\n\n'

			script_strs.append(lines_out)

		funcs.scripts_to_doc(script_strs, doc_filenames)

	else:

		print('No transcript available for this URL...')












