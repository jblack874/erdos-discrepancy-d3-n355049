// Checker B (C, independent): discrepancy of a +/- file over all homogeneous arithmetic progressions.
// usage: edp_checkB file C
#include <stdio.h>
#include <stdlib.h>
int main(int argc,char**argv){FILE*f=fopen(argv[1],"rb");int C=atoi(argv[2]);
 static signed char x[2000001];long n=0;int ch;
 while((ch=fgetc(f))!=EOF){if(ch=='+')x[++n]=1;else if(ch=='-')x[++n]=-1;else if(ch!='\n'&&ch!='\r'){printf("checkB bad char\n");return 2;}}
 int worst=0;long wd=0;
 for(long d=1;d<=n;d++){int s=0;for(long j=d;j<=n;j+=d){s+=x[j];int a=s<0?-s:s;if(a>worst){worst=a;wd=d;}}}
 printf("checkB N=%ld discrepancy=%d (first worst d=%ld) %s at C=%d\n",n,worst,wd,worst<=C?"PASS":"FAIL",C);return worst<=C?0:1;}
