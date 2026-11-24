// Tail backtrack for discrepancy-C sequences. Fixes positions 1..B, runs chronological DFS from B+1,
// preferring the original sign where one exists, else the sign that pulls the divisor sums toward 0.
// usage: edp_tail signsfile C W seed seconds out.txt
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>
static double now(){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec*1e-9;}
int main(int argc,char**argv){
 const char*fn=argv[1];int C=atoi(argv[2]);long W=atol(argv[3]);uint64_t rs=strtoull(argv[4],0,10)*0x9E3779B97F4A7C15ULL+1;double secs=atof(argv[5]);const char*out=argv[6];
 long MAX=500000;signed char*orig=calloc(MAX+2,1),*val=calloc(MAX+2,1),*first=calloc(MAX+2,1),*bestv=calloc(MAX+2,1);unsigned char*st=calloc(MAX+2,1);
 FILE*f=fopen(fn,"rb");long L0=0;int ch;while((ch=fgetc(f))!=EOF){if(ch=='+')orig[++L0]=1;else if(ch=='-')orig[++L0]=-1;}fclose(f);
 int*cnt=calloc(MAX+2,sizeof(int));for(long d=1;d<=MAX;d++)for(long j=d;j<=MAX;j+=d)cnt[j]++;
 long*off=malloc((MAX+2)*sizeof(long));off[1]=0;for(long n=1;n<=MAX;n++)off[n+1]=off[n]+cnt[n];
 int*dv=malloc(off[MAX+1]*sizeof(int));memset(cnt,0,(MAX+2)*sizeof(int));
 for(long d=1;d<=MAX;d++)for(long j=d;j<=MAX;j+=d)dv[off[j]+cnt[j]++]=(int)d;
 int*S=calloc(MAX+2,sizeof(int));long B=L0-W;if(B<0)B=0;
 for(long n=1;n<=B;n++){val[n]=orig[n];for(long q=off[n];q<off[n+1];q++)S[dv[q]]+=val[n];}
 long n=B+1,best=B;st[n]=0;long long nodes=0;double t0=now();int fail=0;
 while(1){
  if((++nodes&1023)==0&&now()-t0>secs)break;
  int x;
  if(st[n]==0){
   if(n<=L0)x=orig[n];
   else{long s=0;for(long q=off[n];q<off[n+1];q++)s+=S[dv[q]];if(s>0)x=-1;else if(s<0)x=1;else{rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;x=(rs&1)?1:-1;}}
   first[n]=(signed char)x;st[n]=1;
  }else if(st[n]==1){x=-first[n];st[n]=2;}
  else{st[n]=0;n--;if(n<=B){fail=1;break;}for(long q=off[n];q<off[n+1];q++)S[dv[q]]-=val[n];val[n]=0;continue;}
  int ok=1;for(long q=off[n];q<off[n+1];q++){int a=S[dv[q]]+x;if(a>C||a<-C){ok=0;break;}}
  if(!ok)continue;
  val[n]=(signed char)x;for(long q=off[n];q<off[n+1];q++)S[dv[q]]+=x;
  if(n>best){best=n;memcpy(bestv+B+1,val+B+1,n-B);}
  n++;if(n>MAX-1)break;st[n]=0;
 }
 memcpy(bestv+1,orig+1,B);
 FILE*o=fopen(out,"w");for(long i=1;i<=best;i++)fputc(bestv[i]>0?'+':'-',o);fclose(o);
 printf("L0=%ld W=%ld B=%ld best_length=%ld gain=%ld nodes=%lld time=%.1fs %s\n",L0,W,B,best,best-L0,nodes,now()-t0,fail?"(window exhausted)":"");
 return 0;}
