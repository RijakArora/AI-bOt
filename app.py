#pip install openai
#pip install pyttsx3
#pip install gtts
#pip install speechRecognition


import speech_recognition as sr
import playsound
import os
import json
import pyttsx3

from gtts import gTTS
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = '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'

client = OpenAI()

male = True

def listen():
	recognizer = sr.Recognizer()
	with sr.Microphone() as source:
		print("Listening...")
		try :
			recognizer.pause_threshold = 0.5
			audio = recognizer.listen(source)
			text = recognizer.recognize_google(audio)
			print("You said -", text)
			return text
		except Exception as e :
			print("Sorry, I could not understand. Error:", e)
			return None

def speak(text):
	print(text)
	speakMS(text)
	#speakGoogle(text)

def speakGoogle(text):
	try:
		print("Speaking...")
		tts = gTTS(text=text, lang='en')
		tts.save("response.mp3")
		playsound.playsound("response.mp3")
	except Exception as e :
		print("Error playing audio:", e)
	if os.path.exists("response.mp3"):
		os.remove("response.mp3")

def speakMS(text):
	global male
	maleVoice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVIV_11.0"
	femaleVoice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
	try:
		print("Speaking...")
		audio = pyttsx3.init()
		audio.setProperty('rate', 150)
		audio.setProperty('volume', 1)
		audio.setProperty('voice', maleVoice if male else femaleVoice)
		audio.say(text)
		audio.runAndWait()
	except Exception as e :
		print("Error playing audio:", e)

def askOnlineAI(text):
	response = client.chat.completions.create(
	  model = "gpt-3.5-turbo-1106",
	  response_format = { "type": "json_object" },
	  messages = [
		{"role": "system", "content": "You are a helpful assistant designed to output JSON."},
		{"role": "user", "content": text}
	  ]
	)
	
	resp = json.loads(response.choices[0].message.content)
	
	for key in resp.keys():
		if key == "error" : 
			return "I don't know about this."
		else :
			return resp[key]
			
def askLlocalAI(text):
	if "how are you feeling" in text.lower():
		return "I am fine , thanks for asking"
	else :
		return False

def substring_after(s, delim):
	return s.partition(delim)[2]
	
def isBlank (myString):
    return not (myString and myString.strip())
	
def main():
	global male
	while True:
		if male:
			assistant = "adam "
		else :
			assistant = "Bell "
		user_input = listen()
		if user_input and assistant in user_input.lower() :
			input = substring_after(user_input.lower(), assistant)
			if "bye bye" in input or "bye-bye" in input :
				response = "Bye-bye, its time to sleep."
				speak(response)
				break
			elif "switch to Bell" in user_input.lower() :
				if male :
					male = False
					response = f"Hey, I'm Bell, How can I help you"
				else : 
					response = "I'm already here"
				speak(response)				
			elif "switch to adam" in user_input.lower() :
				if not male :
					male = True
					response = "Hey, I'm adam, How can I help you"
				else : 
					response = "I'm already here"
				speak(response)				
			elif not isBlank(input) :
				localResponse = askLlocalAI(input)
				if localResponse:
					print("Local AI Says -")
					speak(localResponse)
				else :
					onlineResponse = askOnlineAI(input)
					response = ""
					if isinstance(onlineResponse, list):
						response = " ".join(onlineResponse)
					else :
						response = str(onlineResponse)
					print(assistant)
					speak(response)

if __name__ == "__main__":
    main()