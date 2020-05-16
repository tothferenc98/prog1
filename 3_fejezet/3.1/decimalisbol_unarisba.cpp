#include <iostream>
#include <math.h>
using namespace std;


int main() {

    int a;
    cout<< "Kerek egy szamot"<< endl;
    cin >> a;
    if(a > 0){

        for(int i =0; i< a; i++){
            cout << 1;

        }
    }
    if(a < 0){
        cout << -1;
        for(int i =0; i> a+1; i--){
            cout << 1;

        }

    }
    if(a == 0){
        cout<< "Ilyen szam nem letezik az egyes szamrendszerben"<< endl;
    }


    return 0;
}
