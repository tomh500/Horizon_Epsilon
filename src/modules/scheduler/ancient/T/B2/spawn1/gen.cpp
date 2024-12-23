#include <bits/stdc++.h>
#define fi first
#include <format>
#define se second
using namespace std;
const string path="Horizon/src/modules/scheduler/ancient/T/B2/spawn1";
double sen=2.2;
double m_yaw=0.022;
double m_pitch=0.022;
int N=0;

ofstream fout;

void slp(double x){
    fout<<endl;
    fout<<format("alias syncerReg_delay incrementvar joy_yaw_sensitivity 0 99999999999999 {:.6f}\n",x);
    fout<<format("alias syncer_callback \"exec {}/{}\"\n",path,++N);
    fout<<"syncer_schedule";
    fout=ofstream(format("{}.cfg",N),ios::out);
}
int main(){
    ifstream fin("script.txt",ios::in);
    fout=ofstream("0.cfg",ios::out);
    slp(0.1);

    pair<double,double> lst(-1,-1);

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
            fout<<"yaw 99999999999999999 1 1;\npitch 9999999999999999 1 1;hzCVAR_mouse_std\n";
            lst={0,0};
            slp(0.05);

            pair<double,double> y;
            string s;
            fin>>s>>s>>s>>s>>y.se>>y.fi>>s;

            fout<<format("yaw {:.6f} 1 1\npitch {:.6f} 1 1\n",
                (double)(lst.fi-y.fi)/(sen*m_yaw),
                (double)(y.se-lst.se)/(sen*m_pitch)
            );

            swap(lst,y);

            slp(0.05);
            fout<<"hzCVAR_mouse\n";
        }else if(opt=="END"){
            return 0;
        }else if(opt=="ANG"){
            pair<double,double> y;
            string s;
            fin>>s>>s>>s>>s>>y.se>>y.fi>>s;

            fout<<format("yaw {:.6f} 1 1\npitch {:.6f} 1 1\nhzCVAR_mouse_std\n",
                (double)(lst.fi-y.fi)/(sen*m_yaw),
                (double)(y.se-lst.se)/(sen*m_pitch)
            );

            swap(lst,y);

            slp(0.05);
            fout<<"hzCVAR_mouse\n";
        }
    }
    return 0;
}