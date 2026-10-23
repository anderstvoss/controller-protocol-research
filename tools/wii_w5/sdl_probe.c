#define _GNU_SOURCE
#include <SDL3/SDL.h>
#include <SDL3/SDL_hidapi.h>
#include <dlfcn.h>
#include <fcntl.h>
#include <linux/input.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <float.h>
#include <math.h>
#include <errno.h>
static void(*mark)(const char*);
static void(*register_probe)(int);
static int rawfd=-1;
static uint64_t ms(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return (uint64_t)t.tv_sec*1000+t.tv_nsec/1000000;}
static void pause_ms(unsigned n){struct timespec t={n/1000,(long)(n%1000)*1000000};nanosleep(&t,NULL);}
static void ids(const char*phase){
 if(mark){mark(phase);}printf("{\"kind\":\"ids\",\"phase\":\"%s\",\"banks\":[",phase);
 for(int bank=0;bank<2;bank++){
  unsigned char b[128];for(int i=0;i<200&&read(rawfd,b,sizeof(b))>0;i++){}
  unsigned char req[7]={0x17,4,(unsigned char)(bank?0xa6:0xa4),0,0xfa,0,6};
  int sent=write(rawfd,req,sizeof(req))==(ssize_t)sizeof(req),found=0,reply_error=-1;unsigned char answer[6]={0};uint64_t stop=ms()+800;
  while(sent&&ms()<stop){ssize_t n=read(rawfd,b,sizeof(b));if(n>=6&&b[0]==0x21&&b[4]==0&&b[5]==0xfa&&(b[3]&15)!=0){reply_error=b[3]&15;break;}if(n>=12&&b[0]==0x21&&b[4]==0&&b[5]==0xfa&&(b[3]&15)==0&&(b[3]>>4)==5){memcpy(answer,b+6,6);found=1;reply_error=0;break;}pause_ms(1);}
  printf("%s{\"bank\":\"%s\",\"sent\":%s,\"reply\":%s,\"reply_error\":%d,\"id_hex\":\"",bank?",":"",bank?"a6":"a4",sent?"true":"false",found?"true":"false",reply_error);
  if(found){for(int i=0;i<6;i++){printf("%02x",answer[i]);}}printf("\"}");
 }printf("]}\n");fflush(stdout);
}
static void evdev(int fd,int lo[3],int hi[3],unsigned count[3]){
 if(fd<0){return;}struct input_event events[64];ssize_t n;
 while((n=read(fd,events,sizeof(events)))>0){for(ssize_t i=0;i<n/(ssize_t)sizeof(events[0]);i++){
  struct input_event *e=&events[i];if(e->type==EV_ABS&&e->code>=ABS_RX&&e->code<=ABS_RZ){int a=e->code-ABS_RX;if(e->value<lo[a]){lo[a]=e->value;}if(e->value>hi[a]){hi[a]=e->value;}count[a]++;}
 }}
}
int main(int argc,char**argv){
 if(argc!=4){return 2;}const char*arm=argv[3];int kernel=!strcmp(arm,"kernel"),held=kernel||!strcmp(arm,"holder");
 mark=dlsym(RTLD_DEFAULT,"w5_mark");register_probe=dlsym(RTLD_DEFAULT,"w5_probe_fd");if(!mark||!register_probe){return 3;}mark("child_start");
 rawfd=open(argv[1],O_RDWR|O_NONBLOCK);if(rawfd<0){return 4;}register_probe(rawfd);
 int mpfd=held?open(argv[2],O_RDONLY|O_NONBLOCK):-1;if(held&&mpfd<0){return 5;}
 if(held){mark("holder_open");}else{mark("no_holder");}pause_ms(3000);ids("before_init_api");
 SDL_Joystick*joy=NULL;SDL_Gamepad*pad=NULL;SDL_JoystickID jid=0;bool gyrocap=false,gyroenabled=false,accelcap=false,accelenabled=false;
 if(!kernel){
  SDL_SetHint(SDL_HINT_JOYSTICK_HIDAPI,"1");SDL_SetHint(SDL_HINT_JOYSTICK_HIDAPI_WII,"1");SDL_SetHint(SDL_HINT_JOYSTICK_HIDAPI_WII_PLAYER_LED,"1");SDL_SetHint(SDL_HINT_JOYSTICK_ALLOW_BACKGROUND_EVENTS,"1");
  SDL_SetLogPriority(SDL_LOG_CATEGORY_INPUT,SDL_LOG_PRIORITY_DEBUG);mark("init_api_enter");bool ok=SDL_Init(SDL_INIT_JOYSTICK);mark("init_api_return");if(!ok){return 6;}ids("after_init_api");
  uint64_t deadline=ms()+10000;while(!joy&&ms()<deadline){
   SDL_PumpEvents();SDL_UpdateJoysticks();int count=0;SDL_JoystickID*all=SDL_GetJoysticks(&count);
   for(int i=0;i<count;i++){const char*p=SDL_GetJoystickPathForID(all[i]);if(p&&!strcmp(p,argv[1])){jid=all[i];ids("before_open_api");mark("open_api_enter");joy=SDL_OpenJoystick(jid);mark("open_api_return");ids("after_open_api");break;}}
   SDL_free(all);pause_ms(5);
  }
  if(joy){SDL_InitSubSystem(SDL_INIT_GAMEPAD);pad=SDL_OpenGamepad(jid);}
  if(pad){gyrocap=SDL_GamepadHasSensor(pad,SDL_SENSOR_GYRO);accelcap=SDL_GamepadHasSensor(pad,SDL_SENSOR_ACCEL);accelenabled=accelcap&&SDL_SetGamepadSensorEnabled(pad,SDL_SENSOR_ACCEL,true);gyroenabled=gyrocap&&SDL_SetGamepadSensorEnabled(pad,SDL_SENSOR_GYRO,true);}
  ids("after_sensor_enable");
 }
 int lo[3]={INT32_MAX,INT32_MAX,INT32_MAX},hi[3]={INT32_MIN,INT32_MIN,INT32_MIN};unsigned axis_count[3]={0};
 float glow[3]={FLT_MAX,FLT_MAX,FLT_MAX},ghigh[3]={-FLT_MAX,-FLT_MAX,-FLT_MAX};unsigned samples=0,events=0,nonzero=0,disconnects=0,polls=0;
 uint64_t begin=ms(),window=kernel?20000:60000;int phase=0;mark("drive_start");
 while(ms()-begin<window){
  evdev(mpfd,lo,hi,axis_count);
  if(!kernel){SDL_PumpEvents();SDL_UpdateJoysticks();polls++;if(joy&&!SDL_JoystickConnected(joy)){disconnects++;}
   float v[3];if(gyroenabled&&pad&&SDL_GetGamepadSensorData(pad,SDL_SENSOR_GYRO,v,3)){samples++;int nz=0;for(int i=0;i<3;i++){if(isfinite(v[i])){if(v[i]<glow[i]){glow[i]=v[i];}if(v[i]>ghigh[i]){ghigh[i]=v[i];}if(v[i]!=0){nz=1;}}}nonzero+=nz;}
   SDL_Event e;while(SDL_PollEvent(&e)){if(e.type==SDL_EVENT_GAMEPAD_SENSOR_UPDATE&&e.gsensor.which==jid&&e.gsensor.sensor==SDL_SENSOR_GYRO){events++;}}
  }
  if(phase==0&&ms()-begin>=1000){ids("drive_1s");phase++;}else if(phase==1&&ms()-begin>=10000){ids("drive_10s");phase++;}else if(phase==2&&!kernel&&ms()-begin>=30000){ids("drive_30s");phase++;}else if(phase==3&&!kernel&&ms()-begin>=58000){ids("drive_58s");phase++;}
  pause_ms(5);
 }
 mark("drive_end");ids("after_drive");
 printf("{\"kind\":\"summary\",\"holder\":%s,\"kernel_only\":%s,\"hidapi_open\":%s,\"sdl_version\":%d,\"window_ms\":%llu,\"polls\":%u,\"disconnected_polls\":%u,\"gyro_capable\":%s,\"gyro_enabled\":%s,\"accel_capable\":%s,\"accel_enabled\":%s,\"gyro_samples\":%u,\"gyro_nonzero_samples\":%u,\"gyro_events\":%u,\"gyro_min\":[",held?"true":"false",kernel?"true":"false",joy?"true":"false",SDL_GetVersion(),(unsigned long long)(ms()-begin),polls,disconnects,gyrocap?"true":"false",gyroenabled?"true":"false",accelcap?"true":"false",accelenabled?"true":"false",samples,nonzero,events);
 for(int i=0;i<3;i++){printf("%s%.9g",i?",":"",samples?glow[i]:0.0f);}printf("],\"gyro_max\":[");for(int i=0;i<3;i++){printf("%s%.9g",i?",":"",samples?ghigh[i]:0.0f);}printf("],\"evdev\":[");
 for(int i=0;i<3;i++){printf("%s{\"code\":%d,\"events\":%u,\"min\":%d,\"max\":%d}",i?",":"",ABS_RX+i,axis_count[i],axis_count[i]?lo[i]:0,axis_count[i]?hi[i]:0);}printf("]}\n");fflush(stdout);
 if(pad){SDL_CloseGamepad(pad);}if(joy){SDL_CloseJoystick(joy);}if(!kernel){SDL_Quit();}mark("sdl_closed");
 if(mpfd>=0){close(mpfd);mark("holder_closed");}pause_ms(1500);ids("after_close");register_probe(-1);close(rawfd);mark("child_end");return 0;
}
