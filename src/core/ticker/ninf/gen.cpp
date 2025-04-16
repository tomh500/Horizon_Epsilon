#include <bits/stdc++.h>
using namespace std;
int main(){
    int L=520000;
    int slp=L/0.8;
    int m=25;
    const string us="abcdefghijklmnopqrsuvwxyz";

    for(int i=0;i<m;i++){
        ofstream fout(format("gen/_{}.cfg",i),ios::out|ios::binary);
        for(int j=1;j<=i;j++){
            fout<<"sleep "+to_string(slp)<<'\n';
        }
        fout<<format("hzTicker_ninf_{}_begin\n",i);
        for(int j=1;j<=L;j++){
            fout<<us[i]<<'\n';
        }
        fout.close();
    }

    cout<<"us "<<((slp*m)/1000.0/3600.0)<<endl;

    ofstream fout(format("init.cfg"),ios::out|ios::binary);

    fout<<"alias hzTicker_ninf_clr \"";
    for(int i=0;i<m;i++){
        fout<<format("alias {};",us[i]);
    }
    fout<<"\"\n";
    for(int i=0;i<m;i++){
        fout<<format("alias hzTicker_ninf_{}_begin \"hzTicker_ninf_clr;alias {} $\"\n",i,us[i]);
    }

    fout<<'\n';
    for(int i=0;i<m;i++){
        fout<<format("exec_async Horizon/src/core/ticker/ninf/gen/_{}.cfg\n",i);
    }
}