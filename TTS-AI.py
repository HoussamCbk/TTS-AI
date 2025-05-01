import speech_recognition as sr
import requests
from gtts import gTTS
import os
import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk


DEEPSEEK_API_KEY = 'sk-4f468eb5efbe4315a065d32204fd6c0e'


def translate_text_deepseek(text, dest_lang='en'):
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": f"Translate the following text to {dest_lang}. Return only the translation without any additional text or explanation: {text}"
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            translated_text = response.json()['choices'][0]['message']['content'].strip()
            return translated_text
        else:
            messagebox.showerror("Error", f"Translation failed. Status code: {response.status_code}")
            return text
    except Exception as e:
        messagebox.showerror("Error", f"Translation error: {str(e)}")
        return text


def text_to_speech(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save("presentation_audio.mp3")
        os.system("start presentation_audio.mp3")  
    except Exception as e:
        messagebox.showerror("Error", f"Text-to-Speech error: {e}")


def braille_to_text(braille):
    """Convert Braille dots to text"""
    braille_dict = {
        '⠁': 'a', '⠃': 'b', '⠉': 'c', '⠙': 'd', '⠑': 'e',
        '⠋': 'f', '⠛': 'g', '⠓': 'h', '⠊': 'i', '⠚': 'j',
        '⠅': 'k', '⠇': 'l', '⠍': 'm', '⠝': 'n', '⠕': 'o',
        '⠏': 'p', '⠟': 'q', '⠗': 'r', '⠎': 's', '⠞': 't',
        '⠥': 'u', '⠧': 'v', '⠺': 'w', '⠭': 'x', '⠽': 'y',
        '⠵': 'z', '⠼': '#', '⠪': 'ow', '⠺': 'w', '⠁': 'a',
        '⠂': ',', '⠲': '.', '⠦': '?', '⠖': '!', '⠤': '-',
        '⠄': "'", '⠨': '"', '⠜': 'ar', '⠬': 'gh', '⠮': 'th',
        '⠳': 'ou', '⠩': 'sh', '⠹': 'th', '⠌': '/', '⠀': ' '
    }

    number_dict = {
        '⠁': '1', '⠃': '2', '⠉': '3', '⠙': '4', '⠑': '5',
        '⠋': '6', '⠛': '7', '⠓': '8', '⠊': '9', '⠚': '0'
    }

    try:
        result = []
        number_mode = False
        
        for char in braille:
            if char == '⠼':  
                number_mode = True
                continue
                
            if number_mode and char in number_dict:
                result.append(number_dict[char])
                number_mode = False
            elif char in braille_dict:
                result.append(braille_dict[char])
                number_mode = False
            else:
                result.append(char)
                
        return ''.join(result)
    except Exception as e:
        messagebox.showerror("Error", f"Braille conversion error: {e}")
        return ""

def listen_for_speech(language_menu, languages):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Listening", "Please say something...")
        audio = recognizer.listen(source)
        
    try:
        recognized_text = recognizer.recognize_google(audio)
        messagebox.showinfo("Recognized Speech", f"You said: {recognized_text}")
        

        selected_lang_key = language_menu.get()
        lang_code = languages.get(selected_lang_key, "en")
        translated_text = translate_text_deepseek(recognized_text, dest_lang=lang_code)
        

        text_to_speech(translated_text, lang_code)

    except sr.UnknownValueError:
        messagebox.showerror("Error", "Could not understand the speech.")
    except sr.RequestError as e:
        messagebox.showerror("Error", f"Speech recognition service error: {e}")


def convert_text(language_menu, languages, text_input):
    original_text = text_input.get("1.0", tk.END).strip()
    selected_lang_key = language_menu.get()
    lang_code = languages.get(selected_lang_key, "en")

    if not original_text:
        messagebox.showwarning("Input Error", "Please enter some text.")
        return

    translated_text = translate_text_deepseek(original_text, dest_lang=lang_code)
    text_to_speech(translated_text, lang_code)

def create_ui():
    
    app = ctk.CTk()
    app.title("TTS-AI")
    app.geometry("600x600") 
    app.resizable(True, True)
    app.configure(bg_color="#f2f2f2") 

    frame = ctk.CTkFrame(app, border_width=2, border_color="blue", corner_radius=10)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    label = ctk.CTkLabel(frame, text="Welcome to TTS-AI | Developed by CHOUBIK Houssam", font=("Helvetica", 14))
    label.pack(pady=20)

    label_font = ("Popins", 14, "bold")

    ctk.CTkLabel(app, text="Select Language:", font=label_font).pack(pady=10)

    languages = {
        "English": "en",
        "French": "fr",
        "Spanish": "es",
        "German": "de",
        "Arabic": "ar"
    }

    language_menu = ctk.CTkComboBox(app, values=list(languages.keys()), state="readonly", width=300)
    language_menu.set("English")  
    language_menu.pack(pady=10)

    def option_1_text_to_speech():
        original_text = text_input.get("1.0", "end-1c").strip()
        if original_text:
            text_to_speech(original_text)
        else:
            messagebox.showwarning("Input Error", "Please enter text.")

    def option_2_braille_to_speech():
        braille_input = text_input.get("1.0", "end-1c").strip()
        if not braille_input:
            messagebox.showwarning("Input Error", "Please enter Braille text.")
            return
        
        text = braille_to_text(braille_input)
        if text:
            messagebox.showinfo("Conversion", f"Converted text: {text}")
            text_to_speech(text)
        else:
            messagebox.showerror("Error", "Could not convert Braille input")

    def option_3_translate_text():
        original_text = text_input.get("1.0", "end-1c").strip()
        if original_text:
            selected_lang_key = language_menu.get()
            lang_code = languages.get(selected_lang_key, "en")
            translated_text = translate_text_deepseek(original_text, dest_lang=lang_code)
            messagebox.showinfo("Translation", f"Translated Text: {translated_text}")
        else:
            messagebox.showwarning("Input Error", "Please enter some text.")

    def option_4_text_translation_to_speech():
        original_text = text_input.get("1.0", "end-1c").strip()
        if original_text:
            selected_lang_key = language_menu.get()
            lang_code = languages.get(selected_lang_key, "en")
            translated_text = translate_text_deepseek(original_text, dest_lang=lang_code)
            text_to_speech(translated_text, lang_code)
        else:
            messagebox.showwarning("Input Error", "Please enter some text.")

    def option_5_speech_to_text():
        listen_for_speech(language_menu, languages)

    def option_6_speech_to_text_translation_to_speech():
        listen_for_speech(language_menu, languages)


    button_style = {"width": 200, "height": 30, "fg_color": "#002366", "hover_color": "#219ebc", "font": ("Arial", 12)}


    ctk.CTkButton(app, text="Option 1: Text to Speech", command=option_1_text_to_speech, **button_style).pack(pady=10)
    ctk.CTkButton(app, text="Option 2: Braille to Speech", command=option_2_braille_to_speech, **button_style).pack(pady=10)
    ctk.CTkButton(app, text="Option 3: Translate Text", command=option_3_translate_text, **button_style).pack(pady=10)
    ctk.CTkButton(app, text="Option 4: Translate Text to Speech", command=option_4_text_translation_to_speech, **button_style).pack(pady=10)
    ctk.CTkButton(app, text="Option 5: Speech to Text", command=option_5_speech_to_text, **button_style).pack(pady=10)
    ctk.CTkButton(app, text="Option 6: Speech to Text with Translation to Speech", command=option_6_speech_to_text_translation_to_speech, **button_style).pack(pady=10)


    ctk.CTkLabel(app, text="Enter Text (for Text and Braille to Speech):", font=label_font).pack(pady=10)
    text_input = ctk.CTkTextbox(app, height=100, width=200)
    text_input.pack(pady=10)


    copyright_text = "© 2025 By CHOUBIK Houssam. All Rights Reserved."
    ctk.CTkLabel(app, text=copyright_text, font=("Popins", 12), fg_color="transparent", anchor="center").pack(side="bottom", pady=10)

    app.mainloop()


create_ui()