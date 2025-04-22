#Step 1: Setup Text to Speech–TTS–model 
#with gTTS 
import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language = "en"

    audioobj = gTTS(
        text = input_text,
        lang = language,
        slow = False
    )
    audioobj.save(output_filepath)

input_text = "Hi, this is AI with Sagnik"
#text_to_speech_with_gtts(input_text = input_text, output_filepath = "gtts_testing.mp3")




#Step 2: Use Model for Text output to Voice
import subprocess
import platform

def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    # Removed code that attempted to play audio externally
    return output_filepath # Return the filepath for Gradio


input_text="Hi this is Ai with Hassan, autoplay testing!"
#text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")