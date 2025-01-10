#include <bits/stdc++.h>
using namespace std;
int main(){
    ofstream fout("files/1.cfg",ios::out);
    int m=1500;
    // fout<<"alias %long\n";
    for(int i=1;i<=m;i++){
        fout<<"%long\n";
        fout<<"sleep 10000\n";
    }
    cout<<(m*10)/3600.0;
}