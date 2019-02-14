#include <bits/stdc++.h>
using namespace std;
class ShiftCipher
{
public:
	string cipherMessage(string original,int shift){
		string answer = "";
		for (int i = 0; i < original.size(); ++i){
			if(original[i] == ' '){
				answer+=' ';
				continue;
			}
			char new_char = (((original[i]-65) + shift) % 26) + 65;
			answer+=new_char;
		}
		return answer;
	}
	void initCipher(){
		string message,aux_shift;
		int shift;
		cout << "Enter plain text:\n";
		getline(cin,message);
		cout << "Enter the shift key:\n";
		getline(cin,aux_shift);
		shift = stoi(aux_shift);
		string ciphertext = cipherMessage(message,shift);
		cout << "The ciphertext is:\n";
		cout << ciphertext << endl;
	}

//Decipher	
public:
	string decipher(string ciphertext, int shift){
		string answer = "";
		for (int i = 0; i < ciphertext.size(); ++i){
			if(ciphertext[i] == ' '){
				answer+=' ';
				continue;
			}
			int auxiliar = ((ciphertext[i]-65) - shift);
			while(auxiliar < 0)
				auxiliar+=26;
			char new_char =  auxiliar+ 65;
			answer+=new_char;
		}
		return answer;
	}

	void initDecipher(){
		string aux_shift,message;
		int shift;
		cout << "Enter the ciphertext:\n";
		getline(cin,message);
		cout << "Enter the shift key:\n";
		getline(cin,aux_shift);
		shift = stoi(aux_shift);
		cout << "After deciphering we get:\n";
		cout << decipher(message,shift) << endl;
	}

	void showMenu(){
		string aux_opc;
		int opc;
		while(true){
			while(opc < 1 || opc > 3){
				cout << "Options\n"<<
				"1.- Cipher\n"<<
				"2.- Decipher\n"<<
				"3.- Return to main menu\n";
				getline(cin,aux_opc);
				opc = stoi(aux_opc);
			}
			if(opc == 1)
				initCipher();
			else if(opc == 2)
				initDecipher();
			else{
				break;
			}
			opc = 0;
		}
	}
};