from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
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

        opciones = [self.top_ligues, self.historia, self.algun_cocido, self.putada, self.contar_mayor_paranoia_de_fiesta]
        actual = random.randint(0, 4)
        while actual == self.anterior:
            actual = random.randint(0, 4)
        self.anterior = actual
        opciones[actual]()  # Ejecuta una ronda aleatoria

        texto = f"[Ronda {self.ronda_actual}]\n"
        for j in self.jugadores:
            texto += f"{j.nombre} → {j.puntos} puntos\n"
        self.resultado.text = texto

    def top_ligues(self):
        self.clear_widgets()

        self.puntuaciones_inputs = []

        for jugador in self.jugadores:
            self.add_widget(Label(text=f"Puntuar el ligue que os enseñe  {jugador.nombre}:"))
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
            self.add_widget(Label(text=f"Puntuar historia de {jugador.nombre}:"))
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
            self.add_widget(Label(text=f"¿{jugador.nombre} ha liado alguna (tirar vaso, decir algo inapropiado, etc..)? (0 = no, 1 = sí)"))
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
        self.add_widget(Label(text=f" {elegido.nombre}: cuenta la historia más subrealista que hayas vivido de fiesta si puede ser o que te haya pasado"))
        
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
        self.add_widget(Label(text=f"Puntuar como se ha desembuelto en la putada que habeis elegido para {elegido.nombre}:"))
        
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
