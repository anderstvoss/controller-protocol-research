#include <xwiimote.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <poll.h>
#include <errno.h>
#include <stdint.h>
static long ms(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec*1000+t.tv_nsec/1000000;}
int main(int argc,char**argv){if(argc!=2)return 2;struct xwii_iface*d=NULL;int r=xwii_iface_new(&d,argv[1]);printf("{\"kind\":\"new\",\"result\":%d}\n",r);if(r)return 3;
 unsigned available=xwii_iface_available(d);unsigned mask=XWII_IFACE_CORE|XWII_IFACE_ACCEL|XWII_IFACE_MOTION_PLUS|XWII_IFACE_NUNCHUK;
 r=xwii_iface_open(d,mask);printf("{\"kind\":\"open\",\"result\":%d,\"available\":%u,\"opened\":%u,\"requested\":%u}\n",r,available,xwii_iface_opened(d),mask);fflush(stdout);
 long start=ms();int phase=-1;unsigned events=0;while(ms()-start<18000){int next=(ms()-start)/6000;if(next!=phase){phase=next;if(phase==1)xwii_iface_set_mp_normalization(d,10,20,30,0);if(phase==2)xwii_iface_set_mp_normalization(d,0,0,0,10);printf("{\"kind\":\"phase\",\"phase\":%d}\n",phase);}
 struct pollfd p={.fd=xwii_iface_get_fd(d),.events=POLLIN};poll(&p,1,30);struct xwii_event e;while((r=xwii_iface_dispatch(d,&e,sizeof(e)))==0){events++;if(e.type==XWII_EVENT_MOTION_PLUS||e.type==XWII_EVENT_ACCEL)printf("{\"kind\":\"event\",\"phase\":%d,\"type\":%u,\"v\":[%d,%d,%d]}\n",phase,e.type,e.v.abs[0].x,e.v.abs[0].y,e.v.abs[0].z);}
 if(r!=-EAGAIN){printf("{\"kind\":\"dispatch_error\",\"result\":%d}\n",r);break;}}
 int32_t x,y,z,f;xwii_iface_get_mp_normalization(d,&x,&y,&z,&f);printf("{\"kind\":\"normalization\",\"offsets\":[%d,%d,%d],\"factor\":%d,\"events\":%u}\n",x,y,z,f,events);xwii_iface_unref(d);return 0;}
