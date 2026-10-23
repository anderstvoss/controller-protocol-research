#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/syscall.h>
#include <time.h>
#include <unistd.h>
static ssize_t (*next_read)(int,void*,size_t);
static ssize_t (*next_write)(int,const void*,size_t);
static int log_fd=-1,probe_fd=-1;
static const char *raw_path,*role,*case_name,*arm;
static unsigned long long now_ns(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return (unsigned long long)t.tv_sec*1000000000ULL+t.tv_nsec;}
__attribute__((constructor)) static void init(void){
 next_read=dlsym(RTLD_NEXT,"read");next_write=dlsym(RTLD_NEXT,"write");
 const char*p=getenv("W5_TRACE");if(p){log_fd=open(p,O_WRONLY|O_CREAT|O_APPEND,0600);}
 raw_path=getenv("W5_RAW");role=getenv("W5_ROLE");case_name=getenv("W5_CASE");arm=getenv("W5_ARM");
}
void w5_probe_fd(int fd){probe_fd=fd;}
void w5_mark(const char*label){
 if(log_fd<0){return;}char line[512];int n=snprintf(line,sizeof(line),"{\"ns\":%llu,\"kind\":\"marker\",\"actor\":\"%s\",\"case\":\"%s\",\"arm\":\"%s\",\"label\":\"%s\"}\n",now_ns(),role?role:"provider",case_name?case_name:"none",arm?arm:"none",label);
 if(n>0&&(size_t)n<sizeof(line)){syscall(SYS_write,log_fd,line,(size_t)n);}
}
static unsigned le16(const unsigned char*p){return p[0]|((unsigned)p[1]<<8);}
static void record(int fd,const void*buf,size_t length,int writing){
 if(log_fd<0){return;}char link[64],target[256];snprintf(link,sizeof(link),"/proc/self/fd/%d",fd);
 ssize_t z=readlink(link,target,sizeof(target)-1);if(z<0){return;}target[z]=0;
 const unsigned char*p=buf;size_t size=length;const char*kind;const char*actor;
 if(!strcmp(target,"/dev/uhid")){
  if(length<4){return;}unsigned type=p[0]|((unsigned)p[1]<<8)|((unsigned)p[2]<<16)|((unsigned)p[3]<<24);
  if(writing&&type==12&&length>=6){size=le16(p+4);p+=6;if(size+6>length){return;}kind="device-input";actor="provider";}
  else if(!writing&&type==6&&length>=4103){size=le16(p+4100);p+=4;kind="host-output";actor="aggregate";}
  else{return;}
 }else if(raw_path&&!strcmp(target,raw_path)){
  kind=writing?"raw-output":"raw-input";actor=fd==probe_fd?"probe":"sdl";
 }else{return;}
 if(size>4096){return;}char line[8500];int n=snprintf(line,sizeof(line),"{\"ns\":%llu,\"kind\":\"%s\",\"actor\":\"%s\",\"hex\":\"",now_ns(),kind,actor);
 for(size_t i=0;i<size;i++){n+=snprintf(line+n,sizeof(line)-(size_t)n,"%02x",p[i]);}
 n+=snprintf(line+n,sizeof(line)-(size_t)n,"\"}\n");syscall(SYS_write,log_fd,line,(size_t)n);
}
ssize_t read(int fd,void*p,size_t n){ssize_t r=next_read(fd,p,n);int e=errno;if(r>0){record(fd,p,(size_t)r,0);}errno=e;return r;}
ssize_t write(int fd,const void*p,size_t n){ssize_t r=next_write(fd,p,n);int e=errno;if(r==(ssize_t)n){record(fd,p,n,1);}errno=e;return r;}
