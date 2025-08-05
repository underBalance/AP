from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.metrics import dp, sp
from functools import partial
import random

class Jugador:
    def __init__(self, nombre):
    
        self.nombre = nombre
        self.puntos = 0

class JuegoLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.jugadores = []
        self.num_rondas = 0
        self.ronda_actual = 0
        self.anterior = -1
        #Struct con opciones añadir más conforme aumentes
        self.opciones_completas = [
            self.top_ligues, 
            self.historia, 
            self.algun_cocido, 
            self.putada, 
            self.contar_mayor_paranoia_de_fiesta, 
            self.frase_de_cancion, 
            self.historia_random,
            self.carta_alta,
            self.fisico,
            self.proponer_buen_plan
        ]
        
        self.pruebas_fisicas = [
            "Flexiones",
            "Sentadillas",
            "Dominadas", 
            "Fondos de triceps"
        ]

        
        #La copia, el otro es el original que no se toca.
        self.opciones_disponibles = self.opciones_completas.copy()


        self.entrada_nombre = TextInput(hint_text="Nombre del jugador")
        self.add_widget(self.entrada_nombre)

        self.btn_agregar = Button(text="Agregar jugador")
        self.btn_agregar.bind(on_press=self.agregar_jugador)
        self.add_widget(self.btn_agregar)

        self.btn_jugar = Button(text="Empezar  Juego", disabled=True)
        self.btn_jugar.bind(on_press=self.empezar_juego)
        self.add_widget(self.btn_jugar)

        self.resultado = Label(text="Esperando jugadores...")
        self.add_widget(self.resultado)
        
    def crear_label(self ,texto):
        label = Label(
            text=texto,
            size_hint=(1, None),
            text_size=(Window.width - dp(40), None),
            halign='center',
            valign='middle',
            font_size=sp(16)
        )
        label.bind(texture_size=label.setter('size'))
        return label
    

    def agregar_jugador(self, instance):
        nombre = self.entrada_nombre.text.strip()
        if nombre:
            self.jugadores.append(Jugador(nombre))
            self.entrada_nombre.text = ""
            self.resultado.text = f"Jugador '{nombre}' agregado ({len(self.jugadores)} total)"
        if len(self.jugadores) >= 2:
            self.btn_jugar.disabled = False

    def empezar_juego(self, instance):
        self.clear_widgets()  # ✅ Borra todos los widgets del layout

        self.add_widget(Label(text="Número de rondas:"))
        self.entrada_rondas = TextInput(hint_text="numero de rondas", input_filter = 'int')
        self.add_widget(self.entrada_rondas)
        self.btn_empezar_rondas = Button(text="Empezar rondas")
        self.btn_empezar_rondas.bind(on_press=self.meter_rondas)
        self.add_widget(self.btn_empezar_rondas)

    def meter_rondas(self, instance):
        texto = self.entrada_rondas.text.strip()
        if texto.isdigit():
            self.num_rondas = int(texto)
            self.ronda_actual = 0
            self.resultado = Label(text=f"Se jugarán {self.num_rondas} rondas")
            self.clear_widgets()
            self.add_widget(self.resultado)
            # Aquí puedes empezar a agregar tu lógica de rondas o mostrar botón para jugar rondas
            self.btn_siguiente_ronda = Button(text="▶️ Jugar ronda")
            self.btn_siguiente_ronda.bind(on_press=self.jugar_ronda)
            self.add_widget(self.btn_siguiente_ronda)
        else:
            self.resultado = Label(text="⚠️ Ingresa un número válido de rondas.")
            self.add_widget(self.resultado)

    def jugar_ronda(self, instance):
        self.ronda_actual += 1
        if self.ronda_actual > self.num_rondas:
            self.mostrar_resultado_final()
            return

        if not self.opciones_disponibles:
            self.opciones_disponibles = self.opciones_completas.copy()

        # Filtrar para no repetir la inmediatamente anterior
        opciones_sin_repetir = [f for f in self.opciones_disponibles if f != self.anterior]
        
        if not opciones_sin_repetir:
            opciones_sin_repetir = self.opciones_completas.copy()
        
        actual = random.choice(opciones_sin_repetir)  
        self.opciones_disponibles.remove(actual)
        self.anterior = actual
        actual()
        
        texto = f"[Ronda {self.ronda_actual}]\n"
        for j in self.jugadores:
            texto += f"{j.nombre} → {j.puntos} puntos\n"
        self.resultado.text = texto

    
    
    def top_ligues(self):
        self.clear_widgets()

        self.puntuaciones_inputs = []

        for jugador in self.jugadores:
            #text=f"Puntuar el ligue que os enseñe  {jugador.nombre}:"
           
            self.add_widget(self.crear_label(f"Puntuar el ligue que os enseñe  {jugador.nombre}:"))
            
            entrada = TextInput(input_filter='int', multiline=False)
            self.puntuaciones_inputs.append((jugador, entrada))
            self.add_widget(entrada)

        btn_confirmar = Button(text="Confirmar puntuaciones")
        btn_confirmar.bind(on_press=self.confirmar_puntuaciones_sin_multiplicador)
        self.add_widget(btn_confirmar)

    def confirmar_puntuaciones_sin_multiplicador(self, instance):
        for jugador, entrada in self.puntuaciones_inputs:
            texto = entrada.text.strip()
            if texto.isdigit():
                puntos = int(texto)
                jugador.puntos += puntos
            else:
                # Puedes manejar errores aquí si quieres
                pass

        # Mostrar estado actualizado o avanzar a la siguiente ronda
        self.mostrar_resultado_actualizado()
    
    def confirmar_puntuaciones_con_multiplicador(self, instance, multiplicador):
        for jugador, entrada in self.puntuaciones_inputs:
            texto = entrada.text.strip()
            if texto.isdigit():
                puntos = int(texto) * multiplicador
                jugador.puntos += puntos
            else:
                # Por si quieres dar un valor por defecto o avisar al usuario
                pass
        self.mostrar_resultado_actualizado()

    def mostrar_resultado_actualizado(self):
        self.clear_widgets()
        texto = "Puntos actualizados:\n"
        for jugador in self.jugadores:
            texto += f"{jugador.nombre}: {jugador.puntos} puntos\n"
        self.add_widget(Label(text=texto))

        self.btn_siguiente_ronda = Button(text="▶️ Jugar siguiente ronda")
        self.btn_siguiente_ronda.bind(on_press=self.jugar_ronda)
        self.add_widget(self.btn_siguiente_ronda)
       

    def historia(self):
        self.clear_widgets()
        self.puntuaciones_inputs = []

        for jugador in self.jugadores:
           
            self.add_widget(self.crear_label(f"Puntuar historia de {jugador.nombre}:"))
            entrada = TextInput(input_filter='int', multiline=False)
            self.puntuaciones_inputs.append((jugador, entrada))
            self.add_widget(entrada)

        btn_confirmar = Button(text="Confirmar puntuaciones")
        btn_confirmar.bind(on_press=self.confirmar_puntuaciones_sin_multiplicador)
        self.add_widget(btn_confirmar)
        



    def algun_cocido(self):
        self.clear_widgets()
        self.puntuaciones_inputs = []

        for jugador in self.jugadores:
        
            self.add_widget(self.crear_label(f"¿{jugador.nombre} ha liado alguna (tirar vaso, decir algo inapropiado, etc..)? (0 = no, 1 = sí)"))
            
            entrada = TextInput(input_filter='int', multiline=False)
            self.puntuaciones_inputs.append((jugador, entrada))
            self.add_widget(entrada)

        btn_confirmar = Button(text="Confirmar puntuaciones")
        btn_confirmar.bind(on_press=self.confirmar_puntuaciones_algun_cocido)
        self.add_widget(btn_confirmar)

    def confirmar_puntuaciones_algun_cocido(self, instance):
        for jugador, entrada in self.puntuaciones_inputs:
            texto = entrada.text.strip()
            if texto == '1':
                jugador.puntos -= 5
            elif texto == '0':
                pass  # No cambia puntos
            else:
                # Aquí puedes manejar errores o asignar 0 por defecto
                pass
        self.mostrar_resultado_actualizado()

    def contar_mayor_paranoia_de_fiesta(self):
        self.clear_widgets()
        self.puntuaciones_inputs = []
        
        elegido = random.choice(self.jugadores)
        #text=f" {elegido.nombre}: cuenta la historia más subrealista que hayas vivido de fiesta si puede ser o que te haya pasado"))
     
        self.add_widget(self.crear_label(f"{elegido.nombre}: cuenta la historia más subrealista que hayas vivido de fiesta si puede ser o que te haya pasado"))
                
        entrada = TextInput(input_filter='int', multiline=False)
        self.puntuaciones_inputs.append((elegido, entrada))
        self.add_widget(entrada)
        
        btn_confirmar = Button(text="Confirmar puntuación")
        btn_confirmar.bind(on_press=self.confirmar_puntuaciones_ind)
        self.add_widget(btn_confirmar)

    def putada(self):
        self.clear_widgets()
        self.puntuaciones_inputs = []
        
        elegido = random.choice(self.jugadores)

        self.add_widget(self.crear_label(f"Puntuar como se desembuelve dentro de el reto que le poneis a  {elegido.nombre}:"))
        
        entrada = TextInput(input_filter='int', multiline=False)
        self.puntuaciones_inputs.append((elegido, entrada))
        self.add_widget(entrada)
        
        btn_confirmar = Button(text="Confirmar puntuación")
        btn_confirmar.bind(on_press=self.confirmar_puntuaciones_ind)
        self.add_widget(btn_confirmar)
        
        
    def confirmar_puntuaciones_reto_de_1(self, instance):
        for jugador, entrada in self.puntuaciones_inputs:
            texto = entrada.text.strip()
            if texto == '1':
                jugador.puntos += 5
            elif texto == '0':
                pass  # No cambia puntos
            else:
                # Aquí puedes manejar errores o asignar 0 por defecto
                pass
        self.mostrar_resultado_actualizado()
        
    def carta_alta(self):
        self.clear_widgets()
        self.puntuaciones_inputs = []
        
        elegido = random.choice(self.jugadores)
        #text=f"{elegido.nombre}:  cuenta la historia con un random más graciosa que tengas"
        
        self.add_widget(self.crear_label(f"{elegido.nombre}: adivinar (en caso) de que haya una baraja si la siguiente carta que hay es carta alta o no si lo hace bien 1 sino escribe un 0 y tiene que tomarse un chupito o trago grande"))
        
        entrada = TextInput(input_filter='int', multiline=False)
        self.puntuaciones_inputs.append((elegido, entrada))
        self.add_widget(entrada)
        
        btn_confirmar = Button(text="Confirmar puntuación")
        btn_confirmar.bind(on_press=self.confirmar_puntuaciones_reto_de_1)
        self.add_widget(btn_confirmar)
        
    
    def fisico(self):
        self.clear_widgets()
        self.puntuaciones_inputs = []
        
        elegido = random.choice(self.jugadores)
        #text=f"{elegido.nombre}:  cuenta la historia con un random más graciosa que tengas"
        pruebafisica = random.choice(self.pruebas_fisicas)
        self.add_widget(self.crear_label(f"{elegido.nombre}: te toca hacer {pruebafisica} apuntar cuantas hace"))
        
        entrada = TextInput(input_filter='int', multiline=False)
        self.puntuaciones_inputs.append((elegido, entrada))
        self.add_widget(entrada)
        
        btn_confirmar = Button(text="Confirmar puntuación")
        btn_confirmar.bind(on_press=lambda instance: 
        self.confirmar_puntuaciones_con_multiplicador(instance, 0.7))
        self.add_widget(btn_confirmar)
    
        
    def historia_random(self):
        self.clear_widgets()
        self.puntuaciones_inputs = []
        
        elegido = random.choice(self.jugadores)
        #text=f"{elegido.nombre}:  cuenta la historia con un random más graciosa que tengas"
        
        self.add_widget(self.crear_label(f"Puntuar historia de {elegido.nombre}:"))
        
        entrada = TextInput(input_filter='int', multiline=False)
        self.puntuaciones_inputs.append((elegido, entrada))
        self.add_widget(entrada)
        
        btn_confirmar = Button(text="Confirmar puntuación")
        btn_confirmar.bind(on_press=self.confirmar_puntuaciones_ind)
        self.add_widget(btn_confirmar)
    
    def confirmar_puntuaciones_ind(self, instance):
        for jugador, entrada in self.puntuaciones_inputs:
            texto = entrada.text.strip()
            if texto.isdigit():
                puntos = int(texto)
                jugador.puntos += puntos
            else:
                # Aquí podrías mostrar un error o asignar 0 puntos
                pass
        self.mostrar_resultado_actualizado()
        
    def frase_de_cancion(self):
        self.clear_widgets()
        self.puntuaciones_inputs = []
        
        elegido1 = random.choice(self.jugadores)
        elegido2 = random.choice(self.jugadores)
        while elegido1 == elegido2:
            elegido2 = random.choice(self.jugadores)
            
        self.add_widget(self.crear_label(f"{elegido1.nombre}: tienes que decir una frase de una canción y que la adivine {elegido2.nombre} escribir 1 si la adivina 0 si no."))
        
        entrada = TextInput(input_filter='int', multiline=False)
        self.puntuaciones_inputs.append((elegido1, entrada))
        self.puntuaciones_inputs.append((elegido2, entrada))
        self.add_widget(entrada)
        
        btn_confirmar = Button(text="Confirmar puntuación")
        btn_confirmar.bind(on_press=self.confirmar_puntuaciones_reto_de_1)
        self.add_widget(btn_confirmar)
        
    def proponer_buen_plan(self):
        self.clear_widgets()
        self.puntuaciones_inputs = []
        
        elegido = random.choice(self.jugadores)
        self.add_widget(self.crear_label(f"{elegido.nombre} propone un buen plan si crees que tienes uno mejor de lo que estais haciendo"))
        
        entrada = TextInput(input_filter = 'int', multiline = False)
        self.add_widget(entrada)
        
        self.puntuaciones_inputs.append((elegido, entrada))
        btn_confirmar = Button(text = 'Confirma puntuacion')
        btn_confirmar.bind(on_press= self.confirmar_puntuaciones_reto_de_1)
        self.add_widget(btn_confirmar)
    
    def mostrar_resultado_final(self):
        self.jugadores.sort(key=lambda j: j.puntos, reverse=True)
        texto = "[🏆 Resultados Finales]\n"
        for j in self.jugadores:
            texto += f"{j.nombre}: {j.puntos} puntos\n"
        self.resultado.text = texto
        self.btn_jugar.disabled = True

class JuegoApp(App):
    def build(self):
        return JuegoLayout()

if __name__ == '__main__':
    JuegoApp().run()
