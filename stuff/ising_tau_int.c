/* Metropolis 2D Ising at exact T_c: integrated autocorrelation time of |M|.
   Usage: ising_tau_int L sweeps warmup seed
   Output: L seed sweeps warmup tau_int run_length_in_tau
   tau_int uses Sokal's automatic window (W >= 6 tau). Build: cc -O3 -o ising stuff/ising_tau_int.c -lm
   Infrastructure for cycle 111; the L=256 (>=10 runs) and L=128 (>=1.0M sweeps) runs are NOT done here. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
static uint64_t s[2];
static inline uint64_t rng(void){uint64_t a=s[0],b=s[1],r=a+b;b^=a;s[0]=((a<<55)|(a>>9))^b^(b<<14);s[1]=(b<<36)|(b>>28);return r;}
static inline double u01(void){return (rng()>>11)*(1.0/9007199254740992.0);}
int main(int c,char**v){
  if(c<5){fprintf(stderr,"usage: L sweeps warmup seed\n");return 1;}
  int L=atoi(v[1]);long N=atol(v[2]),W0=atol(v[3]);uint64_t seed=strtoull(v[4],0,10);
  s[0]=seed*0x9E3779B97F4A7C15ULL+1;s[1]=seed^0xD1B54A32D192ED03ULL;for(int i=0;i<20;i++)rng();
  double beta=0.5*log(1.0+sqrt(2.0)),p4=exp(-4*beta),p8=exp(-8*beta);
  signed char*x=malloc(L*L);for(int i=0;i<L*L;i++)x[i]=(rng()&1)?1:-1;
  double*m=malloc(sizeof(double)*N);
  for(long t=0;t<W0+N;t++){
    for(int i=0;i<L;i++)for(int j=0;j<L;j++){
      int k=i*L+j;int nb=x[((i+1)%L)*L+j]+x[((i+L-1)%L)*L+j]+x[i*L+(j+1)%L]+x[i*L+(j+L-1)%L];
      int dE=2*x[k]*nb;
      if(dE<=0||(dE==4&&u01()<p4)||(dE==8&&u01()<p8))x[k]=-x[k];}
    if(t>=W0){long M=0;for(int i=0;i<L*L;i++)M+=x[i];m[t-W0]=fabs((double)M)/(L*L);}
  }
  double mu=0;for(long t=0;t<N;t++)mu+=m[t];mu/=N;
  double c0=0;for(long t=0;t<N;t++)c0+=(m[t]-mu)*(m[t]-mu);c0/=N;
  double tau=0.5;long W;
  for(W=1;W<N/2;W++){double cw=0;for(long t=0;t+W<N;t++)cw+=(m[t]-mu)*(m[t+W]-mu);cw/=(N-W);
    tau+=cw/c0;if(W>=6*tau)break;}
  printf("%d %llu %ld %ld %.3f %.1f\n",L,(unsigned long long)seed,N,W0,tau,N/tau);
  return 0;}
