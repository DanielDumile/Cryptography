#include <bits/stdc++.h>
#include "RandomCipher.h"
#include "ShiftCipher.h"
#include "ModuloTable.h"
#include "ExtendedEuclidean.h"
#include "Affine.h"
//#include "RandomDecipher.h"
using namespace std;

int main(){
	string message,aux_opc;
	
	int opc = 0;
	while(true){
		while(opc > 6 || opc < 1){
			cout << "Menu\n"<<
			"1.- Random Cipher and Decipher\n"<<
			"2.- Shift Cipher and Decipher\n"<<
			"3.- Generate a Table\n"<<
			"4.- Affine cipher\n"<<
			"5.- Extended-Euclidean Algorithm\n"<<
			"6.- Quit\n";
			getline(cin,aux_opc);
			opc = stoi(aux_opc);
		}
		if(opc == 1){
			RandomCipher *rc = new RandomCipher();
			rc->showMenu();
		}
		else if(opc == 2){
			ShiftCipher *sc = new ShiftCipher();
			sc->showMenu();
		}
		else if(opc == 3){
			ModuloTable *t = new ModuloTable();
			t->showMenu();
		}
		else if(opc == 4){
			Affine *a = new Affine();
			a->showMenu();
		}
		else if(opc == 5){
			Euclidean *e = new Euclidean();
			e->showMenu();
		}
		else if(opc == 6){
			cout <<"Goodbye!\n";
			break;
		}
		opc =0;
	}
	return 0;
}