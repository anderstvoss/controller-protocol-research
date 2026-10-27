#define _GNU_SOURCE
#include <dlfcn.h>
#include <fcntl.h>
#include <stdarg.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sys/syscall.h>
static int logfd=-1;static const char*allowed;
__attribute__((constructor))static void init(void){allowed=getenv("W7_ALLOWED");const char*p=getenv("W7_IO_LOG");if(p)logfd=syscall(SYS_openat,AT_FDCWD,p,O_WRONLY|O_CREAT|O_APPEND,0600);}
static int match(const char*p){if(!allowed)return 0;size_t n=strlen(p);const char*q=allowed;while(*q){const char*e=strchr(q,';');size_t len=e?(size_t)(e-q):strlen(q);if(len==n&&!strncmp(p,q,n))return 1;if(!e)break;q=e+1;}return 0;}
static int deny(const char*p){return (!strncmp(p,"/dev/input/",11)||!strncmp(p,"/dev/hidraw",11))&&!match(p);}
static void record(const char*kind,const char*p,int fd){if(logfd<0)return;char b[1024];int n=snprintf(b,sizeof(b),"{\"kind\":\"%s\",\"path\":\"%s\",\"fd\":%d}\n",kind,p,fd);if(n>0&&(size_t)n<sizeof(b))syscall(SYS_write,logfd,b,n);}
static int opening(const char*name,int at,const char*p,int flags,mode_t mode){if(deny(p)){record("blocked-foreign",p,-1);errno=EACCES;return -1;}int r;if(strcmp(name,"openat")){int(*fn)(const char*,int,...)=dlsym(RTLD_NEXT,name);r=fn(p,flags,mode);}else{int(*fn)(int,const char*,int,...)=dlsym(RTLD_NEXT,"openat");r=fn(at,p,flags,mode);}if(match(p))record("owned-open",p,r);return r;}
int open(const char*p,int f,...){mode_t m=0;if(f&O_CREAT){va_list a;va_start(a,f);m=va_arg(a,mode_t);va_end(a);}return opening("open",AT_FDCWD,p,f,m);}int open64(const char*p,int f,...){mode_t m=0;if(f&O_CREAT){va_list a;va_start(a,f);m=va_arg(a,mode_t);va_end(a);}return opening("open64",AT_FDCWD,p,f,m);}int openat(int at,const char*p,int f,...){mode_t m=0;if(f&O_CREAT){va_list a;va_start(a,f);m=va_arg(a,mode_t);va_end(a);}return opening("openat",at,p,f,m);}
ssize_t write(int fd,const void*p,size_t n){ssize_t(*fn)(int,const void*,size_t)=dlsym(RTLD_NEXT,"write");ssize_t r=fn(fd,p,n);int e=errno;char link[64],target[512];snprintf(link,sizeof(link),"/proc/self/fd/%d",fd);ssize_t z=readlink(link,target,sizeof(target)-1);if(z>0){target[z]=0;if(match(target)){char label[128];snprintf(label,sizeof(label),"owned-write-%zu-result-%zd-first-%u",n,r,n?*(const unsigned char*)p:0);record(label,target,fd);}}errno=e;return r;}
struct udev;struct udev_enumerate;struct udev_list_entry;struct udev_device;
static const char*caller(void*addr){Dl_info d;if(dladdr(addr,&d)&&d.dli_fname){const char*p=strrchr(d.dli_fname,'/');return p?p+1:d.dli_fname;}return "unknown";}
static int own_sys(const char*p){const char*raw=getenv("W7_RAW_NAME");return p&&raw&&strstr(p,raw);}
int udev_enumerate_add_match_subsystem(struct udev_enumerate*e,const char*s){int(*fn)(struct udev_enumerate*,const char*)=dlsym(RTLD_NEXT,"udev_enumerate_add_match_subsystem");if(s&&(!strcmp(s,"hidraw")||!strcmp(s,"hid"))){char label[128];snprintf(label,sizeof(label),"enumerate-%s-caller-%s",s,caller(__builtin_return_address(0)));record(label,"metadata-only",0);}return fn(e,s);}
const char*udev_list_entry_get_name(struct udev_list_entry*e){const char*(*fn)(struct udev_list_entry*)=dlsym(RTLD_NEXT,"udev_list_entry_get_name");const char*p=fn(e);if(own_sys(p)){char label[128];snprintf(label,sizeof(label),"owned-enumerated-caller-%s",caller(__builtin_return_address(0)));record(label,p,0);}return p;}
struct udev_device*udev_device_new_from_syspath(struct udev*e,const char*p){struct udev_device*(*fn)(struct udev*,const char*)=dlsym(RTLD_NEXT,"udev_device_new_from_syspath");if(own_sys(p)){char label[128];snprintf(label,sizeof(label),"owned-udev-device-caller-%s",caller(__builtin_return_address(0)));record(label,p,0);}return fn(e,p);}
ssize_t read(int fd,void*p,size_t n){ssize_t(*fn)(int,void*,size_t)=dlsym(RTLD_NEXT,"read");ssize_t r=fn(fd,p,n);int e=errno;if(r>0){char link[64],target[512];snprintf(link,sizeof(link),"/proc/self/fd/%d",fd);ssize_t z=readlink(link,target,sizeof(target)-1);if(z>0){target[z]=0;if(match(target)&&!strncmp(target,"/dev/hidraw",11)){char label[128];snprintf(label,sizeof(label),"owned-read-%zd-first-%u",r,*(unsigned char*)p);record(label,target,fd);}}}errno=e;return r;}
