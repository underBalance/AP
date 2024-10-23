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
int calcularJornada(bool cayoPaya,int calidadPaya,bool asistencia, int calidadAsistencia,bool potaAndGo,bool historiaNoche,int CalidadHistoria){
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
    if(potaAndGo){
        total+=5; //Cinco puntos por pota and go
    }
    if(historiaNoche){
        if(CalidadHistoria>=7){ 
            total+=CalidadHistoria; //Tres puntos por historia de la noche y multiplicador de calidad a partir de 7
        }
        total+=3; //Tres puntos por historia de la noche
    }
    return total;
}

int main(){
    string nombre;
    int calidadPaya, calidadAsistencia, CalidadHistoria;
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
    cout<< "Has conseguido "<< calcularJornada(cayoPaya,calidadPaya,asistencia,calidadAsistencia,potaAndGo,historiaNoche,CalidadHistoria) << " puntos en la jornada de ayer"<< endl;
}