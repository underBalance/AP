#include <iostream>
#include <array>
#include <vector>
#include <iomanip>
#include <string>

using namespace std;

//Lista de ayer con todas las cosas que se pueden hacer en una noche

/*Ligarte un paya o varias (
Seguir hablando con la persona
Pota and go
Asistencias
Historia de la noche
Liado de la noche o puntos por liado
Mañaneo suma
Porros en mañaneo
Cocinar en mañaneo
Ostión 
Intento de le echen de la discoteca 
Que te echen y vuelvas
Colarse en reservado 
Picar copas
Que te inviten a copas
Cerebro de mono bien tirado
Vacile histórico
Librarse de paliza
Comerse chapa resta
Dar chapa resta aún más 
Poner casa para pre
Recoger casa ajena 
Penaliza no hacerlo
Proponer planazo y que salga 
Traer payas
Traer gente que de juego
Dar juego*/

//Se va a implementar ligarte paya, asistencia, pota and go e historia de la noche.
int calcularJornadaLigar(bool cayoPaya,int calidadPaya,bool asistencia, int calidadAsistencia){
    int total=0;
    if(cayoPaya){
        total+=calidadPaya*0.5+3; //Tres puntos por liarte con paya y guapometro en 0.5 max 5 si es un 10
    }
    if(asistencia){
        if(calidadAsistencia<4){  //Resta asistencia mala.
            total-=3; 
        }else{
        total+=calidadAsistencia*0.6+2; //Dos puntos por asistencia y guapometro en 0.6 max 5 si es un 10
        }
    }
   
    return total;
}
int calcularComportamiento(bool potaAndGo, bool historiaNoche, int calidadHistoria){
    int total=0;
    if(potaAndGo){
        total+=2; //Dos puntos por pota and go
    }
    if(historiaNoche){
        if(calidadHistoria<4){ //Resta historia mala.
            total-=3;
        }else{
        total+=calidadHistoria*0.5+2; //Dos puntos por historia de la noche y guapometro en 0.5 max 5 si es un 10
        }
    }
    return total;
}

int main(){
    string nombre;
    int calidadPaya, calidadAsistencia, CalidadHistoria, totalPersona;
    bool cayoPaya, asistencia, potaAndGo, historiaNoche;
    cout << "Introduce tu nombre: "<< endl;
    cin >> nombre;
     cout << "Cayo paya? (1 si, 0 no): "<< endl;
    cin >> cayoPaya;
    if(cayoPaya){
        cout << "Introduce la calidad de la paya: "<< endl;
        cin >> calidadPaya;
    }
    cout << "Hubo asistencia? (1 si, 0 no): "<< endl;
    cin >> asistencia;
    if(asistencia){
    cout << "Introduce la calidad de la asistencia: "<< endl;
    cin >> calidadAsistencia;
    }
    cout << "Hubo pota and go? (1 si, 0 no): "<< endl;
    cin >> potaAndGo;
    cout << "Hiciste la histora de la noche (1 si, 0 no): "<< endl;
    cin >> historiaNoche;
    if(historiaNoche){
    cout << "Introduce la calidad de la historia de la noche: "<< endl;
    cin >> CalidadHistoria;
    }
    totalPersona = calcularJornadaLigar(cayoPaya,calidadPaya,asistencia,calidadAsistencia) ;
    totalPersona += calcularComportamiento(potaAndGo, historiaNoche, CalidadHistoria);
    cout << "" << nombre << ", tu puntuación total de la jornada es: " << totalPersona << endl;
}