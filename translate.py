import json
import azure.cognitiveservices.speech as speech

API_KEY = '63ee143b35fe41449af7901522ac8fb3'
ENDPOINT = "https://ncuazureproject.cognitiveservices.azure.com/"
SPEECH_REGION = "eastus"

languages = ['X','English','Hindi','German','French','Spanish','Italian','Gujrati','Russian','Arabic','Marathi']

from_lang_codes = {'English':'en-US','Hindi':'hi-IN','German':'de-DE','French':'fr-FR',
                   'Spanish':'es-ES','Italian':'it-IT','Gujrati':'gu-IN','Russian':'ru-RU','Marathi':'mr-IN','Arabic':'ar-AE'}

to_lang_codes = {'English':'en','Hindi':'hi','German':'de','French':'fr',
                   'Spanish':'es','Italian':'it','Gujrati':'gu','Russian':'ru','Marathi':'mr','Arabic':'ar'}

voice_codes = {'M':{'English':'en-US-JasonNeural','Hindi':'hi-IN-MadhurNeural','German':'e-DE-BerndNeural','French':'fr-FR-AlainNeural',
                    'Spanish':'es-ES-ArnauNeural','Italian':'it-IT-BenignoNeural','Gujrati':'gu-IN-NiranjanNeural',
                    'Russian':'ru-RU-Dmitry7Neural','Arabic':'ar-AE-HamdanNeural','Marathi':'mr-IN-AarohiNeural'},
                    'F':{'English':'en-US-JennyNeural','Hindi':'hi-IN-SwaraNeural','German':'de-DE-AmalaNeural','French':'fr-FR-BrigitteNeural',
                    'Spanish':'es-ES-AbrilNeural','Italian':'it-IT-ElsaNeural','Gujrati':'gu-IN-DhwaniNeural',
                    'Russian':'ru-RU-DariyaNeural','Arabic':'ar-AE-FatimaNeural','Marathi':'mr-IN-AarohiNeural'}}

translation_config = speech.translation.SpeechTranslationConfig(
    subscription=API_KEY, region=SPEECH_REGION)

print('Choose source language:')
for i in range(1,len(languages)):
    print(i,languages[i])
from_lang_no = int(input(f'Enter 1-{len(languages)-1}:'))
if (from_lang_no<1) or (from_lang_no>len(languages)-1):
    print('Invalid Choice')
    exit()
else:
    from_lang = languages[from_lang_no]

print()

print('Choose target language:')
for i in range(1,len(languages)):
    print(i,languages[i])
to_lang_no = int(input(f'Enter 1-{len(languages)-1}:'))
if (to_lang_no<1) or (to_lang_no>len(languages)-1):
    print('Invalid Choice')
    exit()
else:
    to_lang = languages[to_lang_no]

print()

gender = input('Choose gender(M/F):').upper()
if gender not in ['M','F']:
    print('Invalid choice')
    exit()


from_lang_code = from_lang_codes[from_lang]
to_lang_code = to_lang_codes[to_lang]
voice_code = voice_codes[gender][to_lang]


translation_config.speech_recognition_language = from_lang_code
translation_config.add_target_language(to_lang_code)

audio_config = speech.audio.AudioConfig(use_default_microphone=True)
recognizer = speech.translation.TranslationRecognizer(
    translation_config=translation_config, audio_config=audio_config)

print()
print(f'SPEAK IN {from_lang}!')
print()

result = recognizer.recognize_once()
source_language_text = result.text
duration = result.duration // pow(60, 4)
print(f'{from_lang}({from_lang_code})->{source_language_text}')
print('Duration->',duration,'second(s)')

print()

translation_json = json.loads(result.json)

# to_lang_code = translation_json['Translation']['Translations'][0]['Language']
to_lang_text = translation_json['Translation']['Translations'][0]['Text']
print(f'{to_lang}({to_lang_code})->{to_lang_text}')

speech_config = speech.SpeechConfig(subscription=API_KEY, region=SPEECH_REGION)
audio_config = speech.audio.AudioOutputConfig(use_default_speaker=True)

# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name=voice_code
speech_synthesizer = speech.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

speech_synthesis_result = speech_synthesizer.speak_text_async(to_lang_text)

speech_synthesis_result.get()


