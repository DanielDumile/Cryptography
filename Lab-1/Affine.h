#include <bits/stdc++.h>
using namespace std;
class Affine
{
private:
	//ENE es la pos 13
	string alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ";
	vector<int> inverse;
public:
	void setMultiplicativeInverse(){
		inverse.resize(27);
		//filas
		int nada = 0;
		for (int i = 0; i < 27; ++i){
			//columnas
			for (int j = 0; j < 27; ++j){
				if(!i){
					if(!j){
						nada++;
					}
					else{
						nada++;
					}
				}
				else if(!j){
					nada++;
				}
				else{
					int ans = (i*j) % 27;
					if(ans == 1){
						//cout << "The inverse of " << i << " is " << j << endl;
						inverse[i] = j;
						inverse[j] = i;
					}
				}
			}
		}
	}

	int charToPos(char c){
		int pos = c - 'A';
		//cout << "Pos funcion da " << pos << endl;
		if(pos < 0)
			return 14;
		else if(pos < 14)
			return pos;
		else if(pos >=14)
			return pos+1;
	}

	string getCiphertext(int a,int b,string original){
		string answer="";
		for (int i = 0; i < original.size(); ++i){
			if(original[i] == ' '){
				answer+=' ';
				continue;
			}
			int position = ((a*(charToPos(original[i])))+b)%27;
			//cout << "My position is " << position << endl;
			if(position != 14){
				if(position > 14)
					position++;
				answer+=alphabet[position];
			}
			else
				answer= answer+((char)165);
		}
		return answer;
	}
	void initAffineCipher(){
		int a,b;
		string aux_a,aux_b,message;
		cout << "This affine cipher uses a SPANISH alphabet\n";
		while(true){
			cout << "Enter a:\n";
			getline(cin,aux_a);
			a = stoi(aux_a);
			if(inverse[a])
				break;
			else
				cout << "That value of a does not have a multiplicative inverse\n";
		}
		cout << "Enter b:\n";
		getline(cin,aux_b);
		b = stoi(aux_b);
		cout << "Enter the original message:\n";
		getline(cin,message);
		string ans = getCiphertext(a,b,message);
		cout << "The ciphertext is: " << ans << endl;
	}

	string getOriginal(int a,int b,string ciphertext){
		string answer="";
		for (int i = 0; i < ciphertext.size(); ++i){
			if(ciphertext[i] == ' '){
				answer+=' ';
				continue;
			}
			int position = (((charToPos(ciphertext[i]))-b)*inverse[a]);
			//cout << "Position is " << position << endl;
			while(position < 0)
				position+=27;
			position%=27;

			if(position != 14){
				if(position > 14)
					position++;
				answer+=alphabet[position];
			}
			else
				answer= answer+((char)165);
		}
		return answer;
	}

	void initAffineDecipher(){
		int a,b;
		string aux_a,aux_b,message;
		cout << "This affine cipher uses a SPANISH alphabet\n";
		while(true){
			cout << "Enter a:\n";
			getline(cin,aux_a);
			a = stoi(aux_a);
			if(inverse[a])
				break;
			else
				cout << "That value of a does not have a multiplicative inverse\n";
		}
		
		cout << "Enter b:\n";
		getline(cin,aux_b);
		b = stoi(aux_b);
		cout << "Enter the ciphertext:\n";
		getline(cin,message);
		string ans = getOriginal(a,b,message);
		cout << "The original message is: " << ans << endl;
	}
	void showMenu(){
		string aux_opc;
		int opc;
		setMultiplicativeInverse();
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
				initAffineCipher();
			else if(opc == 2)
				initAffineDecipher();
			else{
				break;
			}
			opc = 0;
		}
	}
	
};