#include <bits/stdc++.h>
#define fi first
#include <format>
#define se second
using namespace std;
const string path="Horizon/src/modules/scheduler/ancient/T/B2/spawn1";
double sen=2.2;
double m_yaw=0.022;
double m_pitch=0.022;
double CVARSLEEP=0.05;
double tickrate=64;
double ticktime=1/tickrate;
int N=0;

ofstream fout;

pair<double,double> lst(-1,-1);

void slp(double x){
    fout<<endl;
    fout<<format("alias syncerReg_delay incrementvar joy_yaw_sensitivity 0 99999999999999 {:.6f}\n",x);
    fout<<format("alias syncer_callback \"exec {}/{}\"\n",path,++N);
    fout<<"syncer_schedule";
    fout=ofstream(format("{}.cfg",N),ios::out);
}

void ang(double x,double y,bool needstd){
    fout<<format("yaw {:.6f} 1 1\npitch {:.6f} 1 1\n",
        (double)(lst.fi-x)/(sen*m_yaw),
        (double)(y-lst.se)/(sen*m_pitch)
    );
    if(needstd) fout<<"hzCVAR_mouse_std\n";

    lst={x,y};

    slp(CVARSLEEP);
    fout<<"hzCVAR_mouse\n";
}

void turntoang(double x,double y,double usetime){
    double ticknum=usetime/ticktime;
    fout<<format("yaw {:.6f} 0 0\npitch {:.6f} 0 0\n",
        (double)(lst.fi-x)/(sen*m_yaw*ticknum),
        (double)(y-lst.se)/(sen*m_pitch*ticknum)
    );
    fout<<"hzCVAR_mouse_std\n";

    lst={x,y};

    slp(usetime);
    fout<<"yaw 0 0 0\npitch 0 0 0\n";
    fout<<"hzCVAR_mouse\n";
}

int main(){
    ifstream fin("script.txt",ios::in);
    fout=ofstream("0.cfg",ios::out);
    slp(CVARSLEEP);


    while(1){
        string opt;
        fin>>opt;
        if(opt=="SRC"){
            string s;
            fin>>s;
            fout<<s<<endl;
        }else if(opt=="SLEEP"){
            double x;
            fin>>x;
            slp(x);
        }else if(opt=="SETANG"){
            fout<<"yaw 99999999999999999 1 1;\npitch 9999999999999999 1 1;\nhzCVAR_mouse_std\n";
            lst={0,0};
            slp(0.05);

            pair<double,double> y;
            string s;
            fin>>s>>s>>s>>s>>y.se>>y.fi>>s;

            ang(y.fi,y.se,0);
        }else if(opt=="ANG"){
            pair<double,double> y;
            string s;
            fin>>s>>s>>s>>s>>y.se>>y.fi>>s;
            
            ang(y.fi,y.se,1);
        }else if(opt=="MOVEANG"){
            pair<double,double> y;
            string s;
            
            double usetime;
            fin>>usetime;
            
            fin>>s>>s>>s>>s>>y.se>>y.fi>>s;

            turntoang(y.fi,y.se,usetime);
        }else if(opt=="END"){
            return 0;
        }
    }
    return 0;
}