#include <bits/stdc++.h>
#define foru(a, b, c) for (int a = (b); (a) <= (c); (a)++)
using namespace std;
const string ID="0123456789abcdefghijklmnopqrstuvwxyz";
int calc(double F,double S){
    return 1000/F+(1000/F)*ceil(S/(1000/F));
}


int dur=4;
int L=95000;
int m='z'-'a';

int MaxFPS=600;
string s="#";

void genInit(){
    ofstream fout("init.cfg",ios::out|ios::binary);

    fout<<format("alias hzTicker_{}_clr \"",s);
    foru(i,0,m-1){
        fout<<format("alias {}{} ;",s,ID[i]);
    }
    fout<<"\"\n\n";

    foru(i,0,m-1){
        fout<<format("alias hzTicker_{}{}_begin \"hzTicker_{}_clr;alias {}{} {}\"\n",s,ID[i],s,s,ID[i],s);
    }

    fout<<"\n\n";
    foru(i,0,m-1){
        fout<<format("exec_async Horizon/src/core/ticker/{}ms/files/_{}.cfg\n",dur,i);
    }
}

int main(){
    if(!filesystem::exists("files")){
        filesystem::create_directories("files");
    }

    const int filetime=L*calc(MaxFPS,dur);

    cerr<<format("filetime {} ms\n",filetime);

    foru(i,0,m-1){
        ofstream fout(format("files/_{}.cfg",i),ios::out|ios::binary);
        foru(j,0,i-1){
            fout<<format("sleep {}\n",filetime);
        }
        fout<<format("hzTicker_{}{}_begin\n",s,ID[i]);
        foru(j,1,L){
            fout<<format("{}{}\nsleep {}\n",s,ID[i],dur);
        }
    }

    cerr<<format("will last for {:.2f} seconds ({:.2f} hours)",filetime*m*1.0/1000.0,filetime*m*1.0/1000.0/3600.0);

    genInit();
    return 0;
}