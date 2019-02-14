#include <bits/stdc++.h>
using namespace std;
class Euclidean
{
public:

	int calculateEuclidean(int a, int b, int & x, int & y) {
	    if (a == 0) {
	        x = 0;
	        y = 1;
	        return b;
	    }
	    int x1, y1;
	    int d = calculateEuclidean(b % a, a, x1, y1);
	    x = y1 - (b / a) * x1;
	    y = x1;
	    return d;
	}

	void initEuclidean(){
		string a_aux,m_aux;
		int a,m,x,y;
		cout << "Enter A:\n";
		getline(cin,a_aux);
		a = stoi(a_aux);
		cout << "Enter M:\n";
		getline(cin,m_aux);
		m = stoi(m_aux);
		int gcd = calculateEuclidean(a,m,x,y);
		cout << "For given A and B, values are\n";
		if(gcd != 1)
			cout <<"There is no multiplicative inverse\n";
		else{
			x = (x % m + m) % m;
			cout << "The multiplicative inverse is " << x << endl;
		}
	}

	void showMenu(){
		string aux_opc;
		int opc;
		while(true){
			while(opc < 1 || opc > 2){
				cout << "Options\n"<<
				"1.- Get the modular inverse of A mod M\n"<<
				//"2.- Get the multiplicative inverse by the Extended Euclidean Algorithm\n"<<
				"2.- Return to main menu\n";
				getline(cin,aux_opc);
				opc = stoi(aux_opc);
			}
			if(opc == 1)
				initEuclidean();
			else{
				break;
			}
			opc = 0;
		}
	}
	
};