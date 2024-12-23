#include <bits/stdc++.h>
#define fi first
#include <format>
#define se second
using namespace std;
int main(){
    ifstream fin("dat.txt",ios::in);
    pair<double,double> x,y;
    string s;
    fin>>s>>s>>s>>s>>x.se>>x.fi>>s;
    fin>>s>>s>>s>>s>>y.se>>y.fi>>s;
    cout<<x.fi<<' '<<x.se<<endl<<y.fi<<' '<<y.se<<endl;

    

    return 0;
}