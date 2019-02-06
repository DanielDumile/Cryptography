#include <bits/stdc++.h>
using namespace std;

namespace patch {
  template <typename T> string to_string(const T& n) {
    ostringstream s;
    s << n;
    return s.str();
  }
}

class RandomCipher
{
private:
	vector<int> mapping;
	unordered_set<int> spaces;
	int size;
	string secret_string;
public:

	void setMessage(string message){
		secret_string="";
		size = message.size();
		mapping.resize(size);

		srand(time(NULL));
		for (int i = 0; i < size; ++i){
			if(message[i] == ' '){
				spaces.insert(i);
				secret_string+=("*,");
				continue;
			}

			mapping[i] = rand() % 26;

			auto aux = patch::to_string(mapping[i]);
			secret_string+=aux;

			if(i != size-1)
				secret_string+=',';
		}
	}

	string cipherMessage(string original){
		string answer = "";
		for (int i = 0; i < size; ++i){
			if(original[i] == ' '){
				continue;
			}
			int shift = mapping[i];
			char new_char = (original[i] + shift) % 26 + 65;
			answer+=new_char;
		}
		return answer;
	}

	string getSecret_string(){
		return secret_string;
	}

	void initCipher(){
		string message;
		cout << "Enter plain text:\n";
		getline(cin,message);
		setMessage(message);
		string ciphertext = cipherMessage(message);
		cout << "The ciphertext is:\n";
		cout << ciphertext << endl;
		cout << "The key is:\n";
		cout << getSecret_string() << endl;
	}

//Decipher	
private:
	int getSize(string s){
		int cont =1;
		for (int i = 0; i < s.size(); ++i){
			if(s[i] == ',')
				cont++;
		}
		return cont;
	}
public:
	string decipherWithString(string ciphertext, string key_string){
		string answer = "";
		int ct_index =0;
		int ms_index =0;
		int size_key = getSize(key_string);
		
		bool space = false;
		for (int i = 0; i < size_key; ++i){

			string string_shift = "";

			while(key_string[ms_index] != ',' && ms_index < key_string.size()){
				//We want to get rid of *
				if(key_string[ms_index] == '*'){
					space = true;
					answer+=' ';
					i++;
					ms_index+=2;
					continue;
				}
				
				string_shift += key_string[ms_index];
				ms_index++;
			}
			ms_index++;//We aint gonna use the next comma
			int shift = stoi(string_shift);//Convert the string_shift into a real number, not string
			char new_char = (ciphertext[ct_index] - shift) % 26 + 65;
			answer+=new_char;
			if(space){
				
			}
			ct_index++;
			space = false;
		}
		return answer;
	}

	void initDecipher(){
		string key,message;
		cout << "Enter the ciphertext:\n";
		getline(cin,message);
		cout << "Enter the key:\n";
		getline(cin,key);
		cout << "After deciphering we get:\n";
		cout << decipherWithString(message,key) << endl;
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