from gensim.parsing.preprocessing import strip_non_alphanum, preprocess_string
from gensim.corpora.dictionary import Dictionary
from keras.models import load_model
import numpy as np
import random
import os
from authentication.models import CustomUser


dir_path = os.path.dirname(os.path.abspath(__file__))  
model_path = os.path.join(dir_path, 'model.h5')

# put chatbot function here

class Chatbot:
    def __init__(self):
        try:
            self.model = load_model(model_path)
        except IOError:
            raise FileNotFoundError("Could not find the model file. Make sure the path is correct.")


        self.finisher = 'It was really nice talking to you and I hope that now you'\
                        ' feel better after talking to me.\nBest of luck for your future '\
                        'endeavors. Bye!'

    def chat(self):
        name = "Student"
        response = '\n\nHello! Thanks for coming here. I am a chatbot. Please let us communicate in English'
        response += f"\nHi {name}! My name's Faraja. Let's start with our session. How are you doing?\n"

        if self.predict(response) >= 0.55:
            response += 'That is good. Are you usually this happy, or are there '\
                        'some worries that you want to talk about?\n'

            if self.predict(response) >= 0.7:
                response += 'You seem to be really content. Wanna sign off?\n'
                if self.predict(response) >= 0.7:
                    return f'Ok, bye {name}!'
                else:
                    response += 'Is there something bothering you? Would you '\
                                'share it with me?\n'
                    if self.predict(response) >= 0.7:
                        return f"That's okay. It was nice talking to you. You can chat "\
                                f"with me anytime you want.\nBye {name}!"
                    else:
                        return self.sad1()
            else:
                return self.sad1()
        else:
            return self.sad3()
