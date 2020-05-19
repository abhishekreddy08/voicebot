# Import the libraries
import platform
import subprocess
import nltk
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import speech_recognition as sr
import os
import pandas as pd
import numpy as np
import pandasql as ps
import word2number
from gtts import gTTS
import datetime
import warnings
import random
import wikipedia
import webbrowser
from genericFunctions import genericFunctions
from ChatterBotChat import VoiceChatBot
from analyticsBot import analyticsBot

# Ignore any warning messages
warnings.filterwarnings('ignore')

gf = genericFunctions()
ab = analyticsBot()


# Function to get the virtual assistant response
def assistantResponse(text):
    print("assistantResponse", text)
    # Convert the text to speech
    msgobj = gTTS(text=text, lang='en', slow=False)
    # Save the converted audio to a file
    msgobj.save('assistant_response.mp3')
    # Play the converted file
    os.system('mpg123 assistant_response.mp3')


if __name__ == "__main__":
    entity = ""
    database_column_existence = False

    generalbot = VoiceChatBot('Example ChatBot')
    trainer = ChatterBotCorpusTrainer(generalbot)
    # Train the chat bot with the entire english corpus
    trainer.train('chatterbot.corpus.english')

    while True:
        # Record the audio
        text = gf.recordAudio()
        response = ''  # Empty response string
        if text is None:
            response = "Sorry my bad. I could not understand you."
            assistantResponse(response)
            continue
            # Checking for the wake word/phrase
        if gf.wakeWord(text):
            # Check for greetings by the user
            response = response + gf.greeting(text)
            # Check to see if the user said date
            str_questions = text[text.find("computer") + 8:]
        else:
            str_questions = text

        if gf.greeting(text):
            response = gf.greeting(text)

        if gf.greetings2(text):
            response = gf.greetings2(text)

        if str_questions == "":
            questions = []
        else:
            questions = str_questions.split("and")

        for i, que in enumerate(questions):
            # response = response + " and answer for question " + str(i + 1) + " is, "
            # print("que :", que)
            print("entity :", entity)
            que = gf.replaceEntity(que, entity, database_column_existence)
            queries = ['employee id', 'employee name', 'employee salary', 'id', 'salary', 'ID', "employee","name"]
            database_column_existence = any(ele in que for ele in queries)
            # print(database_column_existence)
            que = que.lower()
            try:
                if database_column_existence:
                    # print("found column")

                    # df = pd.read_excel("/Users/abhishekreddy/PycharmProjects/voicebot/static/employee_records.xlsx",
                    #                   sheet_name="Sheet1")
                    # nltk.data.show_cfg('/Users/abhishekreddy/PycharmProjects/voicebot/book_grammars/sql1.fcfg')
                    ques = gf.text2int(que)
                    # print("text2int :", ques)
                    q = ab.generateQuery(ques)
                    q = q.replace("[tablename]", "df")
                    # q = '"'+q+'"'
                    print("generateQuery :", q)

                    # print(ps.sqldf(q,locals()))
                    response = gf.readQuery(
                        "/Users/abhishekreddy/PycharmProjects/voicebot/static/employee_records.xlsx", q)
                    wsplit = q.split("where")
                    if len(wsplit) > 0:
                        qsplit = wsplit[1].split("like ")
                        entity = qsplit[1]
                elif 'date' in que:
                    get_date = gf.getDate()
                    response = response + ' ' + get_date
                    # Check to see if the user said time

                elif 'time' in que:
                    now = datetime.datetime.now()
                    meridian = ''
                    if now.hour >= 12:
                        meridian = 'p.m'  # Post Meridian (PM)
                        hour = now.hour - 12
                    else:
                        meridian = 'a.m'  # Ante Meridian (AM)
                        hour = now.hour
                        # Convert minute into a proper string
                    if now.minute < 10:
                        minute = '0' + str(now.minute)
                    else:
                        minute = str(now.minute)
                    response = response + ' ' + 'It is ' + str(hour) + ':' + minute + ' ' + meridian + ' .'

                # Check to see if the user said 'who is'
                elif 'who is' in que:
                    person = gf.getPerson(que)
                    # print("person :", person)
                    wiki = wikipedia.summary(person, sentences=2)
                    response = response + ' ' + wiki
                    entity = person

                elif 'where is' in que:
                    place = gf.getPlace(que)
                    # print("place :", place)
                    wiki = wikipedia.summary(place, sentences=2)
                    response = response + ' ' + wiki
                    entity = place

                elif 'what is' in que:
                    thing = gf.getThing(que)
                    # print("thing :", thing)
                    wiki = wikipedia.summary(thing, sentences=2)
                    response = response + ' ' + wiki
                    entity = thing

                elif 'something about' in que:
                    info = gf.getInfo(que)
                    # print("general :", info)
                    wiki = wikipedia.summary(info, sentences=2)
                    response = response + ' ' + wiki
                    entity = info

                elif 'search google' in que:
                    try:
                        print("You said : {}".format(que))
                        que = que.lower()
                        que = que[que.index("search google")+13:].strip()
                        q = que.split(" ")
                        if(q[0] in ["for","about"]):
                            q = q[1:]
                        que = " ".join(q)
                        url = 'https://www.google.co.in/search?q='
                        search_url = url + que
                        webbrowser.open(search_url)
                    except Exception as e:
                        print("Can't recognize")
                if len(response) == 0:
                    # If response is not known then answer with general bot
                    response = generalbot.get_response(que)

                    if len(response) == 0:
                        response = "Your question was way to much intelligent for me. I am not in mood for it. Ask me to tell a joke instead."
            except wikipedia.DisambiguationError as e:
                # s = random.choice(e.options)
                s = e.options[0]
                response = wikipedia.summary(s)
            except Exception as e:
                response = "Sorry my bad. I could not understand you."
            print("entity: ", entity)
        assistantResponse(response)
