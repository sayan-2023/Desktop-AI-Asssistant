import speech_recognition as sr
import os
import webbrowser
import openai
import win32com.client
from config import apikey

chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Sayan : {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query
    except Exception as e:
        return "Sorry, I'm having trouble accessing the speech recognition service."



def say(text):
         speaker= win32com.client.Dispatch("SAPI.SpVoice")
         speaker.Speak(f" say {text}")

def ai(prompt):
             openai.api_key = apikey
             text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

             response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
    )
             print(response["choices"][0]["text"])
             text += response["choices"][0]["text"]
             if not os.path.exists("Openai"):
                          os.mkdir("Openai")

             with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
                 f.write(text)

if __name__ == '__main__':
             print('Welcome to AI world')
             say(" I am Jarvis AI , How can I help you  ")
             while True:
                 print("Listening...")
                 query = takeCommand()
                 sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],
                          ["spotify","https://open.spotify.com"]]
                 for site in sites:
                     if f"Open {site[0]}".lower() in query.lower():
                                 say(f"Opening {site[0]} sir...")
                                 webbrowser.open(site[1])

                 if "open music" in query.lower():
                          musicPath = r"music\Amplifier.mp3"
                          os.startfile(musicPath)
                 elif "Using artificial intelligence".lower() in query.lower():
                              ai(prompt=query)

                 elif "Jarvis Quit".lower() in query.lower():
                              exit()

                 elif "reset chat".lower() in query.lower():
                            chatStr = ""

                 else:
                    print("Chatting...")
                    chat(query)

