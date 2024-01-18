# Import necessary libraries
from tkinter import *
from tkinter import ttk
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
import speech_recognition as sr
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Create the main Tkinter window
root = Tk()
root.geometry('1100x500')
root.resizable(0, 0)
root.title("Language Translator")
root.config(bg='lightgray')

# Heading
Label(root, text="LANGUAGE TRANSLATOR", font="arial 20 bold", bg='lightgray').pack(pady=10)

# Input and Output Text Widgets
Label(root, text="Enter Text or Speak", font='arial 13 bold', bg='lightgray').place(x=200, y=60)
Input_text = Text(root, font='arial 10', height=8, wrap=WORD, padx=5, pady=5, width=60)
Input_text.place(x=30, y=100)

Label(root, text="Output", font='arial 13 bold', bg='lightgray').place(x=780, y=60)
Output_text = Text(root, font='arial 10', height=8, wrap=WORD, padx=5, pady=5, width=60)
Output_text.place(x=600, y=100)

# Language Selection
Label(root, text="Select Input Language", font='arial 10 bold', bg='lightgray').place(x=20, y=60)
src_lang = ttk.Combobox(root, values=list(LANGUAGES.values()), width=22)
src_lang.place(x=20, y=80)
src_lang.set('english')

Label(root, text="Select Output Language", font='arial 10 bold', bg='lightgray').place(x=890, y=60)
dest_lang = ttk.Combobox(root, values=list(LANGUAGES.values()), width=22)
dest_lang.place(x=890, y=80)
dest_lang.set('english')

# Define translation function
def translate():
    translator = Translator()
    translated = translator.translate(text=Input_text.get(1.0, END), src=src_lang.get(), dest=dest_lang.get())
    Output_text.delete(1.0, END)
    Output_text.insert(END, translated.text)

# Translate Button
trans_btn = Button(root, text='Translate', font='arial 12 bold', pady=5, command=translate, bg='royal blue1',
                   activebackground='sky blue')
trans_btn.place(x=490, y=180)

# Text to Speech function for Output Text
def output_text_to_speech():
    text = Output_text.get(1.0, END)
    if text:
        output_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'output.mp3')
        tts = gTTS(text=text, lang='en')  # Use 'en' for English
        tts.save(output_path)
        sound = pygame.mixer.Sound(output_path)
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))  # Wait for the sound to finish

# Text to Speech Button for Output Text
tts_output_btn = Button(root, text='Output to Speech', font='arial 12 bold', pady=5, command=output_text_to_speech, bg='purple',
                        activebackground='violet')
tts_output_btn.place(x=780, y=450)

# Text to Speech function for Input Text
def text_to_speech():
    text = Input_text.get(1.0, END)
    if text:
        output_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'output.mp3')
        tts = gTTS(text=text, lang='en')  # Use 'en' for English
        tts.save(output_path)
        sound = pygame.mixer.Sound(output_path)
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))  # Wait for the sound to finish

# Text to Speech Button for Input Text
tts_input_btn = Button(root, text='Text to Speech', font='arial 12 bold', pady=5, command=text_to_speech, bg='green',
                 activebackground='lime')
tts_input_btn.place(x=50, y=450)

# Speech to Text function
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language=src_lang.get())
            Input_text.delete(1.0, END)
            Input_text.insert(END, text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")


root.mainloop()
