/* Cycle 110, member-2: 2-D Ising Metropolis tau_int of |M| at exact T_c.
   Usage: ising_tau_c110 L sweeps warmup seed  -> prints "L seed tau_int N/tau"
   Seeds: 110000 + 100*L + run (new in cycle 110). Sokal window, c=6. */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
static uint64_t s[2];
static inline uint64_t rotl(uint64_t x,int k){return (x<<k)|(x>>(64-k));}
static inline uint64_t nxt(void){uint64_t a=s[0],b=s[1],r=a+b;b^=a;s[0]=rotl(a,55)^b^(b<<14);s[1]=rotl(b,36);return r;}
int main(int c,char**v){int L=atoi(v[1]);long N=atol(v[2]),W=atol(v[3]);uint64_t sd=strtoull(v[4],0,10);
 s[0]=sd*0x9E3779B97F4A7C15ULL+1;s[1]=sd^0xD1B54A32D192ED03ULL;for(int i=0;i<20;i++)nxt();
 double K=0.5*log(1+sqrt(2.0));uint64_t th[5];for(int d=0;d<5;d++){double p=exp(-2*K*(2*d));th[d]=p>=1?UINT64_MAX:(uint64_t)(p*18446744073709551615.0);}
 int n=L*L;signed char*sp=malloc(n);for(int i=0;i<n;i++)sp[i]=1;long M=n;double*x=malloc(sizeof(double)*N);
 for(long t=-W;t<N;t++){for(int i=0;i<n;i++){int r=i/L,q=i%L;int h=sp[r*L+(q+1)%L]+sp[r*L+(q+L-1)%L]+sp[((r+1)%L)*L+q]+sp[((r+L-1)%L)*L+q];
   int e=sp[i]*h; /* dE=2*K*e ; e in -4..4 */ if(e<=0||nxt()<th[e/2]){sp[i]=-sp[i];M+=2*sp[i];}}
   if(t>=0)x[t]=fabs((double)M)/n;}
 double m=0;for(long t=0;t<N;t++)m+=x[t];m/=N;double c0=0;for(long t=0;t<N;t++)c0+=(x[t]-m)*(x[t]-m);c0/=N;
 double tau=0.5;for(long k=1;k<N/2;k++){double ck=0;for(long t=0;t+k<N;t++)ck+=(x[t]-m)*(x[t+k]-m);ck/=(N-k);tau+=ck/c0;if(k>=6*tau)break;}
 printf("%d %llu %.3f %.0f\n",L,(unsigned long long)sd,tau,N/tau);return 0;}
