import sys
import os
import openai
import requests
from PIL import Image
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr

# Set up the OpenAI API client
openai.api_key = os.getenv('OPENAI_API_KEY')
# Set up the model and prompt
model_engine = "text-davinci-003"
#model_engine = "text-ada-001"
#model_engine = "gpt-3.5-turbo"

def print_intro():
  print("\n")
  print("\n")
  print("\n")
  print("|-------------------------------------------------------------------------|\n")
  print("|-- WELCOME -- CHATGPT TE LLEVA AL LÍMITE DEL CONOCIMIENTO: BIG DATA Y IA |\n")
  print("|                                                                         |\n")
  print("| Javier Lahoz Sevilla: https://www.linkedin.com/in/fcojavierlahoz        |\n")
  print("| - Head of Big Data Engineering en Orange                                |\n")
  print("| - Profesor de Data & IA en ESIC                                         |\n")
  print("|-------------------------------------------------------------------------|\n")
  print("\n")
  print("\n")
  print("\n")
  print("\n")
  print("\n")

def call(model_engine,prompt):
  # Generate a response
  completion = openai.Completion.create(
      engine=model_engine,
      prompt=prompt,
      max_tokens=2048,
      n=3,
      stop=None,
      temperature=0.5,
  )
  return completion.choices[0].text

def run_chat():
  while(True):
    prompt = input('Soy ChatGPT, ¿que quieres saber?\n')
    if prompt == "":
      break
    response = call(model_engine,prompt)
    print(response)
    print("\n")
    myobj = gTTS(text=response, lang="es", tld="es", slow=False)
    myobj.save("tmp/tmp.mp3")
    playsound("tmp/tmp.mp3")

def run_chat_prompt(prompt):
    response = call(model_engine,prompt)
    print(response)
    print("\n")
    myobj = gTTS(text=response, lang="es", tld="es", slow=False)
    myobj.save("tmp/tmp.mp3")
    playsound("tmp/tmp.mp3")

def run_voice():
  r = sr.Recognizer()
  while(True):
    with sr.Microphone() as source:
      print("Talk")
      audio_text = r.listen(source)
      print("Time over, thanks")
      try:
        # using google speech recognition
        text = r.recognize_google(audio_text,language = "es-ES, en-EN")
        print("Text: "+text)
        run_chat_prompt(text)
      except:
        print("Sorry, I did not get that")        
      if text == "adiós":
        break

def run_prompt(prompt):
  print(prompt)
  response = call(model_engine,prompt)
  print(response)
  print("\n")

def run_image(prompt):
  print(prompt)
  response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="512x512"
  )
  url = response['data'][0]['url']
  img_data = requests.get(url).content
  with open('tmp/tmp.jpg', 'wb') as handler:
    handler.write(img_data)
      
  img = Image.open("tmp/tmp.jpg")
  img.show()

def run(option,prompt):
  match option:
    case "chat":
      run_chat()
    case "prompt":
      run_prompt(prompt)
    case "image":
      run_image(prompt)
    case "voice":
      run_voice()
    case "help":
      print("Usage: nothing or chat, voice, prompt <Text>, image <Text>")
    case _:
      print("Bad Option: help, nothing or chat, voice, prompt, image")

if __name__ == "__main__":
  #print_intro()
  if len(sys.argv) == 2:
    option =  sys.argv[1]   
    prompt = ""
  elif len(sys.argv) == 3:
    option =  sys.argv[1]   
    prompt = sys.argv[2]
    if prompt == "":
      prompt = "Test"
  else:
    option = "chat"
    prompt = ""
  run(option,prompt)

