# Import the libraries
import speech_recognition as sr
import datetime
import warnings
import calendar
import random
import pandas as pd
import pandasql as ps
# Ignore any warning messages
warnings.filterwarnings('ignore')


class genericFunctions(object):
    # Record audio and return it as a string
    def recordAudio(self):
        # Record the audio
        r = sr.Recognizer()
        r.energy_threshold = 5000
        with sr.Microphone() as source:
            print('Say something!')
            audio = r.listen(source)
        # Speech recognition using Google's Speech Recognition
        data = ''
        try:
            data = r.recognize_google(audio)
            print("You said : {}".format(data))
        except sr.UnknownValueError:
            print('Google Speech Recognition could not understand')
            return None
        except sr.RequestError as e:
            print('Request error from Google Speech Recognition')
            return None
        except Exception as e:
            print(e)
            return None
        return data

    def dfToString(self,df):
        resultshape = df.shape
        finaltext = "Result received. " + str(resultshape[0]) + " records " + " with " + str(resultshape[1]) + " columns "
        cols = df.columns
        for (idx, row) in df.iterrows():
            finaltext = finaltext + ". Result " + str(idx + 1) + " is, "
            for i, col in enumerate(cols):
                if (i > 0):
                    finaltext = finaltext + " and "
                finaltext = finaltext + " " + str(col) + " " + str(row.loc[col])
        return finaltext

    def readQuery(self, filepath, query):
        df = pd.read_excel(filepath,
                           sheet_name="Sheet1")

        resultdf = ps.sqldf(query, locals())
        return self.dfToString(resultdf)
    # A function to check for wake word(s)
    def wakeWord(self, text):
        WAKE_WORDS = ['hello computer']
        text = text.lower()  # Convert the text to all lower case words
        # Check to see if the users command/text contains a wake word
        for phrase in WAKE_WORDS:
            if phrase in text:
                return True
        # If the wake word was not found return false
        return False

    # A function to get current date
    def getDate(self):
        now = datetime.datetime.now()
        my_date = datetime.datetime.today()
        weekday = calendar.day_name[my_date.weekday()]  # e.g. Monday
        monthNum = now.month
        dayNum = now.day
        month_names = ['January', 'February', 'March', 'April', 'May',
                       'June', 'July', 'August', 'September', 'October', 'November',
                       'December']
        ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th',
                          '7th', '8th', '9th', '10th', '11th', '12th',
                          '13th', '14th', '15th', '16th', '17th',
                          '18th', '19th', '20th', '21st', '22nd',
                          '23rd', '24th', '25th', '26th', '27th',
                          '28th', '29th', '30th', '31st']

        return 'Today is ' + weekday + ' ' + month_names[monthNum - 1] + ' the ' + ordinalNumbers[dayNum - 1] + '.'

    # Function to return a random greeting response
    def greeting(self, text):
        # Greeting Inputs
        GREETING_INPUTS = ['hi', 'hey', 'hola', 'greetings', 'wassup', 'hello']
        # Greeting Response back to the user
        GREETING_RESPONSES = ['howdy', 'whats good', 'hello', 'hey there']
        # If the users input is a greeting, then return random response
        for word in text.split():
            if word.lower() in GREETING_INPUTS:
                hour = int(datetime.datetime.now().hour)
                if 0 <= hour < 12:
                    resp = "Good Morning"
                elif 12 <= hour < 18:
                    resp = "Good Afternoon"
                else:
                    resp = "Good Evening"

                iam = "Please tell me how may I help you"

                return random.choice(GREETING_RESPONSES) + '.' + resp + '.' + iam
        # If no greeting was detected then return an empty string
        return ''

    def greetings2(self, text):
        # Greeting Inputs
        SENDOFF_INPUTS = ['okay bye', 'bye', 'see you', 'catch you later', 'ok bye']
        THANK_INPUT = ['Thanks', 'Thank you']
        # Greeting Response back to the user
        SENDOFF_RESPONSES = ['bye bye', 'see you', 'catch you later', 'will be waiting for you!', 'come back soon',
                             'nice talking to you']
        THANK_RESPONSE = ['Mention not']
        # If the users input is a greeting, then return random response
        for word in text.split():
            if word.lower() in SENDOFF_INPUTS:
                return random.choice(SENDOFF_RESPONSES) + '.'
            if word.lower() in THANK_INPUT:
                return random.choice(THANK_RESPONSE) + '.'

        # If no greeting was detected then return an empty string
        return ''

    # Function to get a person first and last name
    def getPerson(self, text):
        text = text.lower()
        keyword = 'who is'
        before_keyword, keyword, after_keyword = text.partition(keyword)
        return after_keyword

    def getPlace(self, text):
        text = text.lower()
        keyword = 'where is'
        before_keyword, keyword, after_keyword = text.partition(keyword)
        return after_keyword

    def getThing(self, text):
        text = text.lower()
        keyword = 'what is'
        before_keyword, keyword, after_keyword = text.partition(keyword)
        return after_keyword

    def getInfo(self, text):
        text = text.lower()
        keyword = 'something about'
        before_keyword, keyword, after_keyword = text.partition(keyword)
        return after_keyword

    def text2int(self, textnum):
        scale_dict = {"hundred": 100, "thousand": 1000, "lakh": 100000, "lac": 100000, "million": 1000000,
                      "billion": 1000000000, "trillion": 1000000000000}

        text_s = textnum.split(" ")
        new_text = []
        for i, t in enumerate(text_s):

            if t in scale_dict:
                if text_s[i - 1].isdigit():
                    value = int(text_s[i - 1]) * scale_dict[t]
                    new_text = new_text[:-1]
                else:
                    value = scale_dict[t]

                # print("value", value)
                new_text.append(str(value))

            elif (len(new_text) > 0 and len(text_s) > i + 1 and new_text[-1].isdigit() and t.isdigit()
                  and (text_s[i + 1].isdigit() or text_s[i + 1] in scale_dict)):

                new_text.append(t)
            elif len(new_text) > 0 and new_text[-1].isdigit() and t.isdigit():
                value = int(new_text[-1]) + int(t)
                new_text = new_text[:-1]
                new_text.append(str(value))
            else:
                new_text.append(t)

            #print(new_text)

        final_text = []
        for i, t in enumerate(new_text):
            if len(final_text) > 0 and final_text[-1].isdigit() and t.isdigit():
                if int(final_text[-1]) <= int(t):
                    value = int(final_text[-1]) * int(t)
                else:
                    value = int(final_text[-1]) + int(t)
                final_text = final_text[:-1]
                final_text.append(str(value))
            else:
                final_text.append(t)
        # print(final_text)
        curstring = " ".join(final_text)
        return curstring

    def replaceEntity(self, que, entity, database_column_existence):
        qwords = que.split(" ")
        ewords = ["he", "she", "it", "his", "her", "its", "him"]
        foundentityref = False
        for i, w in enumerate(qwords):
            if w in ewords and database_column_existence:
                qwords[i] = ""
                foundentityref=True
            if w in ewords and not database_column_existence:
                # que = que.replace(i, entity)
                qwords[i] = entity

        que = " ".join(qwords)
        if database_column_existence and foundentityref:
            que = que + " for "+entity[1:-1]
        print("replaced que :", que)
        return que
