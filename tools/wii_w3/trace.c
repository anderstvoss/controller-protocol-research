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
static ssize_t (*real_read)(int,void*,size_t);
static ssize_t (*real_write)(int,const void*,size_t);
static int trace_fd=-1;
__attribute__((constructor)) static void init(void){
 real_read=dlsym(RTLD_NEXT,"read");real_write=dlsym(RTLD_NEXT,"write");
 const char *path=getenv("W3_TRACE");if(path)trace_fd=open(path,O_WRONLY|O_CREAT|O_APPEND,0600);
}
static unsigned le16(const unsigned char*p){return p[0]|((unsigned)p[1]<<8);}
static void record(int fd,const void*data,size_t length,int outgoing){
 if(trace_fd<0||length<4)return;
 char path[64],target[128];snprintf(path,sizeof(path),"/proc/self/fd/%d",fd);
 ssize_t n=readlink(path,target,sizeof(target)-1);if(n<0)return;target[n]=0;if(strcmp(target,"/dev/uhid"))return;
 const unsigned char*p=data;unsigned kind=p[0]|((unsigned)p[1]<<8)|((unsigned)p[2]<<16)|((unsigned)p[3]<<24);
 const char *direction;size_t size;
 if(outgoing&&kind==12&&length>=6){size=le16(p+4);p+=6;direction="device-input";if(size+6>length)return;}
 else if(!outgoing&&kind==6&&length>=4103){size=le16(p+4100);p+=4;direction="host-output";}
 else return;
 if(size>4096)return;
 struct timespec ts;clock_gettime(CLOCK_MONOTONIC,&ts);
 char line[8400];int used=snprintf(line,sizeof(line),"{\"ns\":%llu,\"direction\":\"%s\",\"hex\":\"",(unsigned long long)ts.tv_sec*1000000000ULL+ts.tv_nsec,direction);
 for(size_t i=0;i<size;i++)used+=snprintf(line+used,sizeof(line)-(size_t)used,"%02x",p[i]);
 used+=snprintf(line+used,sizeof(line)-(size_t)used,"\"}\n");syscall(SYS_write,trace_fd,line,(size_t)used);
}
ssize_t read(int fd,void*data,size_t n){ssize_t result=real_read(fd,data,n);int saved=errno;if(result>0)record(fd,data,(size_t)result,0);errno=saved;return result;}
ssize_t write(int fd,const void*data,size_t n){ssize_t result=real_write(fd,data,n);int saved=errno;if(result==(ssize_t)n)record(fd,data,n,1);errno=saved;return result;}
