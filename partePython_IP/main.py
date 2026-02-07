"""
Copyright (c) 2026 Gabriel Olmedilla Barrientos
Licensed under the MIT License.
"""


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.metrics import dp, sp
from functools import partial
import random
import json



class JuegoLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.players = []
        self.impostors= []
        self.index = 0
        
        self.hints = False
        self.actual_hint=""
        self.actual_word=""
        self.num_of_impostors=0
        
        self.actual_case = None
        self.actual_word = ""
        self.actual_hint = ""

        with open("words.json", "r") as f:
            self.words_data = json.load(f)
        
        self.start_game(None)
        
        
    def create_label(self ,text):
        label = Label(
            text=text,
            size_hint=(1, None),
            text_size=(Window.width - dp(40), None),
            halign='center',
            valign='middle',
            font_size=sp(16)
        )
        label.bind(texture_size=label.setter('size'))
        return label
    
    def start_game(self, instance):
        self.clear_widgets()
        self.entry_player_name = TextInput(hint_text="Player name")
        self.add_widget(self.entry_player_name)

        self.add_btn = Button(text="Add player")
        self.add_btn.bind(on_press=self.add_player)
        self.add_widget(self.add_btn)

        self.play_btn = Button(text="Start game", disabled=True)
        self.play_btn.bind(on_press=self.hints_and_num_impostors)
        self.add_widget(self.play_btn)

        self.result = Label(text="Waiting for players...")
        self.add_widget(self.result)

    def add_player(self, instance): #Instance not  used but needed by Kivy for some reason.
        nombre = self.entry_player_name.text.strip()
        if nombre:
            self.players.append(nombre)
            self.entry_player_name.text = ""
            self.result.text = f"Added player '{nombre}', total: ({len(self.players)})"
        if len(self.players) >= 2:
            self.play_btn.disabled = False

    def hints_and_num_impostors(self, instance):
        self.clear_widgets()  # Erase widgets.

        self.add_widget(Label(text="Game format:"))
        uses_hints = TextInput(hint_text="If the game is going to use Hints, write 1 if not 0.", input_filter = 'int')
        self.add_widget(uses_hints)
        if uses_hints:
            self.hints = True
        else:
            self.hints = False
        self.btn_empezar_rondas = Button(text="Select number of impostors")
        self.btn_empezar_rondas.bind(on_press=self.number_of_impostors)
        self.add_widget(self.btn_empezar_rondas)

    def number_of_impostors(self, instance):
        self.clear_widgets()
        self.add_widget(Label(text="Number of impostors:"))
        self.num_of_impostors_input = TextInput(hint_text="Write the number of impostors:", input_filter = 'int')
        self.add_widget(self.num_of_impostors_input)
        
        self.btn_empezar_rondas = Button(text="Confirm and start playing")
        self.btn_empezar_rondas.bind(on_press=self.confirm_number_of_impostors)
        self.add_widget(self.btn_empezar_rondas)

    def confirm_number_of_impostors(self, instance):
        value = self.num_of_impostors_input.text.strip()

        if not value:
            print("You must enter a number")
            return

        num = int(value)

        if num < 1:
            print("There must be at least 1 impostor")
            return

        if num >= len(self.players):
            print("Too many impostors")
            return

        self.num_of_impostors = num


        self.round(instance)


    def round(self, instance):
        self.clear_widgets()
        #Decide impostors
        self.impostors = random.sample(
            self.players,
            self.num_of_impostors
        )
        #Decide word:
        self.actual_case = random.choice(list(self.words_data.values()))
        self.actual_word = self.actual_case["word"]
        self.actual_hint = self.actual_case["hint"]
        
        #Logic to show each player their role and word
        self.index=0
        self.show_player(instance)
        
    def show_player(self, instance):
        if self.index < len(self.players):
            self.clear_widgets()
            player = self.players[self.index]
            self.btn_word = Button(text=f"Player: {player}")  
            self.btn_word.bind(
                on_press=lambda instance, p=player: self.show_word(instance, p)
            )
            self.index = self.index + 1 
            self.add_widget(self.btn_word)
        else:
            self.clear_widgets()
            self.btn_next_round = Button(text=f"Next round")  
            self.btn_next_round.bind(on_press=self.round)
            self.btn_start_again = Button(text="Start again")
            self.btn_start_again.bind(on_press=self.start_game)
            self.add_widget(self.btn_next_round)
            self.add_widget(self.btn_start_again)

    def show_word(self, instance, player):
        self.clear_widgets()
        if player in self.impostors:
            self.add_widget(Label(text="Impostor !!"))
            if self.hints:
                self.add_widget(Label(text=f"Hint: {self.actual_hint}"))
        else:
            self.add_widget(Label(text=f"Civil, the word is: {self.actual_word}"))
            
        self.btn_back = Button(text="Back")
        self.btn_back.bind(on_press=self.show_player)
        self.add_widget(self.btn_back)        
        
        
class JuegoApp(App):
    def build(self):
        return JuegoLayout()

if __name__ == '__main__':
    JuegoApp().run()
