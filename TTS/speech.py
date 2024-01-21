import speech_recognition
import pyttsx3

## pip install pyttsx3 remove later, for documentation purposes
## pip install py3-tts

class TextToSpeech:
    
        def __init__(self):
            pass

        def text_to_speech(self, text):
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()

class VoiceRecognition:

    def __init__(self):
        pass

    def speech_to_text(self):
        recognizer = speech_recognition.Recognizer()

        while True:
            try:
                with speech_recognition.Microphone() as mic:

                    recognizer.adjust_for_ambient_noise(mic, duration=0.1)
                    audio = recognizer.listen(mic)

                    text = recognizer.recognize_google(audio)
                    text = text.lower()

                    print(f"Recognized {text}") # ! ! ! for testing purposes only, remove after words
                    return text

            except speech_recognition.UnknownValueError():

                recognizer = speech_recognition.Recognizer()
                continue

# usage
Speech = VoiceRecognition()
bob = Speech.speech_to_text()
Text = TextToSpeech()
Text.text_to_speech(bob)