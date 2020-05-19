import platform
import subprocess
from chatterbot import ChatBot


class VoiceChatBot(ChatBot):

    def speak(self, text):
        if platform.system() == 'Darwin' or 'Linux' or 'Java' or 'Windows':
            # Use Mac's built-in say command to speak the response
            cmd = ['speak', str(text)]

            subprocess.call(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        else:
            subprocess.run(
                'echo "' + str(text) + '" | festival --tts',
                shell=True
            )

    def get_response(self, statement=None, **kwargs):
        resp = super().get_response(statement, **kwargs)
        # self.speak(response.text)
        print("get resp", resp)
        return resp.text