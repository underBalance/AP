#include <iostream>
#include <array>
#include <vector>
#include <iomanip>
#include <string>
#include <algorithm> // para std::sort

using namespace std;

struct Jugador {
    string nombre;
    int puntos;
};
struct Jugadores {
    int numJugadores;
    vector<Jugador> jugadores;
};

void llenarJugadores(Jugadores &jugadores, int numJugadores) {
    for (int i = 0; i < numJugadores; i++) {
        Jugador jugador;
        cout << "Ingrese el nombre del jugador " << (i + 1) << ": ";
        cin >> jugador.nombre;
        jugador.puntos = 0; // Inicializar puntos a 0
        jugadores.jugadores.push_back(jugador);
    }
    jugadores.numJugadores = numJugadores;
}

void jugarRonda(Jugadores &jugadores, int numRondas) {
    /*Aqui voy a hacer solo una implementacion del modo de juego.*/
    for(jugadores.numJugadores = 0; jugadores.numJugadores < jugadores.jugadores.size(); jugadores.numJugadores++) {
       cout << "Puntuar historia de " << jugadores.jugadores[jugadores.numJugadores].nombre << ": ";
       cin >> jugadores.jugadores[jugadores.numJugadores].puntos;
    }
}

string visualizarRonda(const Jugadores &jugadores) {
    string resultado;
    for (const auto &jugador : jugadores.jugadores) {
        resultado += jugador.nombre + ": " + to_string(jugador.puntos) + " puntos\n";
    }
    return resultado;
}

void jugarRondas(Jugadores &jugadores, int numRondas){
    for (int ronda = 1; ronda <= numRondas; ronda++) {
        cout << "Ronda " << ronda << endl;
        jugarRonda(jugadores, ronda);
        cout << "Resultados de la ronda " << ronda << ":" << visualizarRonda(jugadores) << endl;
    }
    //Mostrar ranking final
    cout << "Ranking final:" << endl;
    std::sort(jugadores.jugadores.begin(), jugadores.jugadores.end(),
    [](const Jugador& a, const Jugador& b) {
        return a.puntos > b.puntos; // mayor a menor
    });
    for (const auto& jugador : jugadores.jugadores) {
    std::cout << jugador.nombre << " → " << jugador.puntos << " puntos\n";
}

}






int main() { 
    string nombres, nombreHistoria;

    int numRondas, numJugadores, puntosTotales;
    int cantidadCervezas, puntosHistoria, calidadHistoria;
    struct Jugadores jugadores;
    
    cout << "Ingrese num de rondas para jugar: ";
    cin >> numRondas;
    cout << "Ingrese num de jugadores: ";
    cin >> numJugadores;
    if (numJugadores < 2 ) {
        cout << "El numero de jugadores debe ser minimo 2" << endl;
        return 1;
    }

    llenarJugadores(jugadores, numJugadores);
    jugarRondas(jugadores, numRondas);
    return 0;

}