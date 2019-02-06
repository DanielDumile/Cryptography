#include <bits/stdc++.h>
using namespace std;
class Affine
{
private:
	string alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	vector<int> inverse;
public:
	void setMultiplicativeInverse(){
		inverse.resize(26);
		//filas
		int nada = 0;
		for (int i = 0; i < 26; ++i){
			//columnas
			for (int j = 0; j < 26; ++j){
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
					int ans = (i*j) % 26;
					if(ans == 1){
						cout << "The inverse of " << i << " is " << j << endl;
						inverse[i] = j;
						inverse[j] = i;
					}
				}
			}
		}
	}
	string getCiphertext(int a,int b,string original){
		string answer="";
		for (int i = 0; i < original.size(); ++i){
			if(original[i] == ' '){
				answer+=' ';
				continue;
			}
			int position = ((a*(original[i]-65))+b)%26;
			answer+=alphabet[position];
		}
		return answer;
	}
	void initAffineCipher(){
		int a,b;
		string aux_a,aux_b,message;
		cout << "This affine cipher uses a ENGLISH alphabet\n";
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
			int position = (((ciphertext[i]-65)-b)*inverse[a]);
			//cout << "Position is " << position << endl;
			while(position < 0)
				position+=26;
			position%=26;
			answer+=alphabet[position];
		}
		return answer;
	}

	void initAffineDecipher(){
		int a,b;
		string aux_a,aux_b,message;
		cout << "This affine cipher uses a ENGLISH alphabet\n";
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