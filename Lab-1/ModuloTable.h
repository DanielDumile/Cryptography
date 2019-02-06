#include <bits/stdc++.h>
using namespace std;
typedef pair<int,int> pii;

class ModuloTable
{
public:
	
	vector<int> primes;
	vector<bool> isPrime;

	void primesSieve(int n){
		isPrime.resize(n + 1, true);
		isPrime[0] = isPrime[1] = false;
		primes.push_back(2);
		for(int i = 4; i <= n; i += 2) 
			isPrime[i] = false;
		int limit = sqrt(n);
		for(int i = 3; i <= n; i += 2){
			if(isPrime[i]){
				primes.push_back(i);
				if(i <= limit)
					for(int j = i * i; j <= n; j += 2 * i)
						isPrime[j] = false;
			}
		}
	}
	vector<int> factorize(int n){
		vector<int> factores;
		for(int primo : primes){
			//Si nuestro primo^2 es mayor a nuestra n, significa que ya no es factir y todos los siguientes
			//no lo seran igual. Entonces no tiene caso seguir con el for
			if(primo * primo > n) 
				break;
			int power = 0;
			//Si nuestra n es divisible por nuestro primo
			while(n % primo == 0){
				power++;
				//dividimos a nuestra n para hacerla mas chica y contar los divisores
				n /= primo;
			}
			//Si ese primo si pudo dividir a n, osea n%primo ==0 almenos una vez
			if(power) 
				factores.push_back(primo);
		}
		//Si nuestra n termino sin cambios, o llego a ser un numero primo despues de las divisiones
		//entonces agregamos a esa n a nuestro vector de resultado
		if(n > 1)
			factores.push_back(n);
		return factores;
	}

	void getMultiplos(int n,vector<int> factores, unordered_set<int> &no_usar){
		for (int i = 1; i <n; ++i){
			for(auto f : factores){
				if(!(i%f) && i != f)
					no_usar.insert(i);
			}
		}
	}

	void showMenu(){
		int n;
		while(true){
			string aux_opc;
			int opc;
			while(opc < 1 || opc > 2){
				cout << "Options\n"<<
				"1.- Single number n\n"<<
				//"2.- Enter the number and its k prime factors\n"<<
				"2.- Return to main menu\n";
				getline(cin,aux_opc);
				opc = stoi(aux_opc);
			}
			if(opc == 2){
				break;
			}
			else{
				int n;
				string aux_n;
				cout << "Enter the number\n";
				getline(cin,aux_n);
				n = stoi(aux_n);
				primesSieve(n);
				unordered_set<int> no_usar;
				if(opc == 1){
					if(!isPrime[n]){
						auto factores = factorize(n);
						cout << "Its prime factors are: \n";
						for(auto p: factores){
							cout << p << endl;
							no_usar.insert(p);
						}
						getMultiplos(n,factores,no_usar);
						cout << "We wont be using the next numbers:" << endl;
						for(auto n: no_usar){
							cout << n << " ";
						}
						cout << endl;
					}
					else 
						cout << "Its a prime!" << endl;

					//filas
					for (int i = 0; i < n; ++i){
						//columnas
						if(no_usar.count(i))
						 	continue;
						for (int j = 0; j < n; ++j){
							if(no_usar.count(j))
							 	continue;
							if(!i){
								if(!j){
									cout << "   ";
								}
								else{
									if(j < 10)
										cout << "0";
									cout << j << " ";
								}
							}
							else if(!j){
								if(i < 10)
									cout << "0";
								cout << i << " ";
							}
							else{
								int res = (i*j) % n;
								if(res < 10)
									cout << "0";
								cout << res << " ";
							}
						}
						cout << "\n";
					}
					cout <<"\n";
				}

				
			}
			opc=0;
		}
		
	}

};