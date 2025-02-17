#include <bits/stdc++.h>
using namespace std;
ofstream fout("result.cfg",ios::out);
int t[20]={0,0,20,40,60,80,100,120,140,160,180,200,240,280,360,400,440,520};
int n=17;
void solve(int l,int r){
    if(l>r) return ;
    string lc="cMotSyncer_RL_Ajudge_ret";
    string rc="cMotSyncer_RL_Ajudge_ret";
    int p=(l+r)>>1;
    if(p-1>=l){
        lc=format("cMotSyncer_RL_Ajudge_{}",t[(l+p-1)>>1]);
    }
    if(p+1<=r){
        rc=format("cMotSyncer_RL_Ajudge_{}",t[(p+1+r)>>1]);
    }
    fout<<format("alias cMotSyncer_RL_Ajudge_{} \"cMotSyncer_RL_A2D;incrementvar tv_timeout 0 {:4f} 0;cMotSyncer_RL_D2T;alias 0] cMotSyncer_RL_Ajudge_{}_nxt;alias cMotSyncer_RL_Ajudge_nxt {};cMotSyncer_RL_Tchk0;cMotSyncer_RL_Ajudge_nxt\"",t[p],t[p]*1.0/1000,t[p],lc)<<endl;
    fout<<format("alias cMotSyncer_RL_Ajudge_{}_nxt \"alias cMotSyncer_RL_Ajudge_ret cMotSyncer_RL_Ajudge_{}_ret;alias cMotSyncer_RL_Ajudge_nxt {}\"",t[p],t[p],rc)<<endl;
    fout<<endl;
    solve(l,p-1);
    solve(p+1,r);
}
int main(){

    solve(1,n);

    return 0;
}