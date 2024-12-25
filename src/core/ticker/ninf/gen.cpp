#include <bits/stdc++.h>
using namespace std;
int main(){
    int slp=515000;
    int N=22;
    ofstream init("init.cfg",ios::out);
    ofstream clr("clr/clr.cfg",ios::out);

    for(int i=1;i<=N;i++){
        clr<<format("alias hzTickerManager_ninf_loop_{} \"{}alias $ hzTickerManager_ninf_loop_{}\"\n",i,i==1?"$trig;":"",i+1==N+1?1:i+1);
        ofstream clr_to1(format("clr/clr{}_to1.cfg",i),ios::out);
        clr_to1<<format("alias hzTickerManager_ninf_loop_{} \"{}alias $ hzTickerManager_ninf_loop_1\"\n",i,i==1?"$trig;":"");
    }
    for(int i=1;i<=N;i++){
        init<<format("alias hzTickerManager_ninf_loop_{} \"{}alias $ hzTickerManager_ninf_loop_{}\"\n",i,i==1?"$trig;":"",i+1==N+1?1:i+1);
    }
    init<<'\n';
    init<<format("alias hzTickerManager_ninf_load_0 \"say 计时终止 需要重启游戏\"\n");
    for(int i=1;i<=N;i++){
        init<<format("alias hzTickerManager_ninf_load_{} \"alias hzTickerManager_ninf_add hzTickerManager_ninf_load_{};alias hzTickerManager_ninf_rmv hzTickerManager_ninf_load_{};exec Horizon/src/core/ticker/ninf/clr/clr;exec Horizon/src/core/ticker/ninf/clr/clr{}_to1;\"\n",i,i+1,i-1,i);
    }
    init<<"alias hzTickerManager_ninf_add hzTickerManager_ninf_load_1\n";
    init<<"alias $ hzTickerManager_ninf_loop_1\n";

    init<<'\n';
    for(int i=1;i<=N;i++){
        init<<format("exec_async Horizon/src/core/ticker/ninf/file/_{}.cfg\n",i);
    }

    for(int o=1;o<=N;o++){
        ofstream fout(format("file/_{}.cfg",o),ios::out|ios::binary);
        for(int i=1;i<o;i++){
            fout<<format("sleep {}\n",slp);
        }
        fout<<"hzTickerManager_ninf_add"<<'\n';
        for(int i=1;i<=520000;i++){
            fout<<"$"<<'\n';
        }
        fout<<"hzTickerManager_ninf_rmv"<<'\n';
    }
    cout<<format("will last {:.5f}h",N*slp*1.0/1000.0/3600.0);
    return 0;
}