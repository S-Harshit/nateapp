import json
import azure.cognitiveservices.speech as speech
from flask import Flask, render_template, request
app = Flask(__name__, template_folder="templates", static_folder="static")

API_KEY = '93dae62e87e5454bac23f17debc93af3'
ENDPOINT = "https://msazureproject.cognitiveservices.azure.com/"
SPEECH_REGION = "eastus"



# languages = ['X','English','Hindi','German','French','Spanish','Italian','Gujrati','Russian','Arabic','Marathi']


voice_codes = {'M':{'English':'en-US-JasonNeural','Hindi':'hi-IN-MadhurNeural','German':'de-DE-BerndNeural','French':'fr-FR-AlainNeural',
                        'Spanish':'es-ES-ArnauNeural','Italian':'it-IT-BenignoNeural','Gujarati':'gu-IN-NiranjanNeural',
                        'Russian':'ru-RU-DmitryNeural','Arabic':'ar-AE-HamdanNeural','Marathi':'mr-IN-AarohiNeural'},
                        'F':{'English':'en-US-JennyNeural','Hindi':'hi-IN-SwaraNeural','German':'de-DE-AmalaNeural','French':'fr-FR-BrigitteNeural',
                        'Spanish':'es-ES-AbrilNeural','Italian':'it-IT-ElsaNeural','Gujarati':'gu-IN-DhwaniNeural',
                        'Russian':'ru-RU-DariyaNeural','Arabic':'ar-AE-FatimaNeural','Marathi':'mr-IN-AarohiNeural'}}
    
to_lang_codes = {'English':'en','Hindi':'hi','German':'de','French':'fr',
                   'Spanish':'es','Italian':'it','Gujarati':'gu','Russian':'ru','Marathi':'mr','Arabic':'ar'}
    
from_lang_codes = {'English':'en-US','Hindi':'hi-IN','German':'de-DE','French':'fr-FR',
                   'Spanish':'es-ES','Italian':'it-IT','Gujarati':'gu-IN','Russian':'ru-RU','Marathi':'mr-IN','Arabic':'ar-AE'}

# global from_lang
def translate_speech(from_lang,to_lang,gender):

    translation_config = speech.translation.SpeechTranslationConfig(
        subscription=API_KEY, region=SPEECH_REGION)
    
    global voice_code
    voice_code = voice_codes[gender][to_lang]
    to_lang_code = to_lang_codes[to_lang]
    from_lang_code = from_lang_codes[from_lang]

    translation_config.speech_recognition_language = from_lang_code
    translation_config.add_target_language(to_lang_code)

    audio_config = speech.audio.AudioConfig(use_default_microphone=True)
    recognizer = speech.translation.TranslationRecognizer(
        translation_config=translation_config, audio_config=audio_config)

    result = recognizer.recognize_once()
    global from_lang_text
    from_lang_text = result.text
    global duration
    duration = result.duration // pow(60, 1)

    translation_json = json.loads(result.json)

    # to_lang_code = translation_json['Translation']['Translations'][0]['Language']
    global to_lang_text
    to_lang_text = translation_json['Translation']['Translations'][0]['Text']

    return from_lang,to_lang,from_lang_text,to_lang_text,duration

    # The language of the voice that speaks.

def text_to_speech():
    speech_config = speech.SpeechConfig(subscription=API_KEY, region=SPEECH_REGION)
    audio_config = speech.audio.AudioOutputConfig(use_default_speaker=True)

    global voice_code
    speech_config.speech_synthesis_voice_name=voice_code
    speech_synthesizer = speech.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    global to_lang_text
    speech_synthesis_result = speech_synthesizer.speak_text_async(to_lang_text)
    speech_synthesis_result.get()

    


@app.route("/", methods=["GET", "POST"])
def index():
    print(request.form)
    if ('listen' in request.form):
        text_to_speech()
        # print('HELLO')
        global from_lang
        global to_lang
        global from_lang_text
        global to_lang_text
        global duration
        return render_template("result.html", from_lang=from_lang,to_lang=to_lang,from_lang_text=from_lang_text,to_lang_text=to_lang_text,duration=duration)
    elif(request.method == "POST"):
        from_lang = request.form.get('src_lang')
        to_lang = request.form.get('tar_lang')
        gender = request.form.get('gender')
        from_lang,to_lang,from_lang_text,to_lang_text,duration = translate_speech(from_lang,to_lang,gender)
        return render_template("result.html", from_lang=from_lang,to_lang=to_lang,from_lang_text=from_lang_text,to_lang_text=to_lang_text,duration=duration)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()

