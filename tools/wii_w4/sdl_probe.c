#include <SDL3/SDL.h>
#include <SDL3/SDL_hidapi.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <float.h>
#include <stdint.h>

typedef struct { unsigned samples; float low[3], high[3]; } Sensor;
static void sensor_init(Sensor *s) {
    s->samples=0; for(int i=0;i<3;i++){s->low[i]=FLT_MAX;s->high[i]=-FLT_MAX;}
}
static void sensor_sample(Sensor *s, SDL_Gamepad *p, SDL_SensorType type, bool enabled) {
    float v[3]; if(!enabled || !p || !SDL_GetGamepadSensorData(p,type,v,3))return;
    for(int i=0;i<3;i++){if(!isfinite(v[i]))return;}
    for(int i=0;i<3;i++){if(v[i]<s->low[i])s->low[i]=v[i];if(v[i]>s->high[i])s->high[i]=v[i];}s->samples++;
}
static void sensor_print(const char *name,Sensor *s,bool capable,bool enabled) {
    printf("\"%s\":{\"capable\":%s,\"enabled\":%s,\"samples\":%u,\"min\":[",name,capable?"true":"false",enabled?"true":"false",s->samples);
    for(int i=0;i<3;i++)printf("%s%.9g",i?",":"",s->samples?s->low[i]:0.0f);
    printf("],\"max\":[");for(int i=0;i<3;i++)printf("%s%.9g",i?",":"",s->samples?s->high[i]:0.0f);printf("]}");
}
int main(int argc,char **argv) {
    if(argc!=2)return 2;
    SDL_SetHint(SDL_HINT_JOYSTICK_HIDAPI,"1");SDL_SetHint(SDL_HINT_JOYSTICK_HIDAPI_WII,"1");
    SDL_SetHint(SDL_HINT_JOYSTICK_HIDAPI_WII_PLAYER_LED,"1");SDL_SetHint(SDL_HINT_JOYSTICK_ALLOW_BACKGROUND_EVENTS,"1");
    SDL_SetLogPriority(SDL_LOG_CATEGORY_INPUT,SDL_LOG_PRIORITY_DEBUG);
    if(!SDL_Init(SDL_INIT_JOYSTICK|SDL_INIT_GAMEPAD))return 3;
    struct SDL_hid_device_info *devs=SDL_hid_enumerate(0x057e,0x0306);int enumerated=0,raw_open=0;
    for(struct SDL_hid_device_info *d=devs;d;d=d->next)if(!strcmp(d->path,argv[1])){
        enumerated++;SDL_hid_device *r=SDL_hid_open_path(d->path);raw_open=r!=NULL;if(r)SDL_hid_close(r);
    }SDL_hid_free_enumeration(devs);
    SDL_Joystick *joy=NULL;SDL_Gamepad *pad=NULL;SDL_JoystickID id=0;
    Uint64 deadline=SDL_GetTicks()+10000;
    while(!joy && SDL_GetTicks()<deadline){
        SDL_PumpEvents();SDL_UpdateJoysticks();int count=0;SDL_JoystickID *ids=SDL_GetJoysticks(&count);
        for(int i=0;i<count;i++){const char *p=SDL_GetJoystickPathForID(ids[i]);if(p&&!strcmp(p,argv[1])){id=ids[i];joy=SDL_OpenJoystick(id);break;}}
        SDL_free(ids);SDL_Delay(5);
    }
    if(!joy){printf("{\"owned_hid_count\":%d,\"raw_open\":%s,\"hidapi_open\":false}\n",enumerated,raw_open?"true":"false");SDL_Quit();return 4;}
    pad=SDL_OpenGamepad(id);
    bool ac=pad&&SDL_GamepadHasSensor(pad,SDL_SENSOR_ACCEL),gc=pad&&SDL_GamepadHasSensor(pad,SDL_SENSOR_GYRO);
    bool ae=ac&&SDL_SetGamepadSensorEnabled(pad,SDL_SENSOR_ACCEL,true),ge=gc&&SDL_SetGamepadSensorEnabled(pad,SDL_SENSOR_GYRO,true);
    bool led1=SDL_SetJoystickPlayerIndex(joy,1),led2=false;bool ledcap=SDL_GetBooleanProperty(SDL_GetJoystickProperties(joy),SDL_PROP_JOYSTICK_CAP_PLAYER_LED_BOOLEAN,false);
    int axes=SDL_GetNumJoystickAxes(joy),buttons=SDL_GetNumJoystickButtons(joy);if(axes>32||buttons>64||axes<0||buttons<0)return 5;
    int amin[32],amax[32];unsigned bseen[64]={0};for(int i=0;i<32;i++){amin[i]=32767;amax[i]=-32768;}
    Sensor accel,gyro;sensor_init(&accel);sensor_init(&gyro);
    unsigned polls=0,disconnected=0,removed=0,axis_events=0,button_events=0,sensor_events=0;
    Uint64 begin=SDL_GetTicks();
    while(SDL_GetTicks()-begin<60000){
        SDL_PumpEvents();SDL_UpdateJoysticks();polls++;if(!SDL_JoystickConnected(joy))disconnected++;
        if(!led2 && SDL_GetTicks()-begin>=30000)led2=SDL_SetJoystickPlayerIndex(joy,2);
        for(int i=0;i<axes;i++){int v=SDL_GetJoystickAxis(joy,i);if(v<amin[i])amin[i]=v;if(v>amax[i])amax[i]=v;}
        for(int i=0;i<buttons;i++)bseen[i]|=SDL_GetJoystickButton(joy,i)?2:1;
        sensor_sample(&accel,pad,SDL_SENSOR_ACCEL,ae);sensor_sample(&gyro,pad,SDL_SENSOR_GYRO,ge);
        SDL_Event e;while(SDL_PollEvent(&e)){
            if(e.type==SDL_EVENT_JOYSTICK_REMOVED && e.jdevice.which==id)removed++;
            if(e.type==SDL_EVENT_JOYSTICK_AXIS_MOTION && e.jaxis.which==id)axis_events++;
            if((e.type==SDL_EVENT_JOYSTICK_BUTTON_DOWN||e.type==SDL_EVENT_JOYSTICK_BUTTON_UP)&&e.jbutton.which==id)button_events++;
            if(e.type==SDL_EVENT_GAMEPAD_SENSOR_UPDATE&&e.gsensor.which==id)sensor_events++;
        }SDL_Delay(5);
    }
    printf("{\"sdl_version\":%d,\"owned_hid_count\":%d,\"raw_open\":%s,\"hidapi_open\":true,\"window_ms\":%llu,\"polls\":%u,\"disconnected_polls\":%u,\"removed_events\":%u,\"axis_events\":%u,\"button_events\":%u,\"sensor_events\":%u,\"axes\":[",SDL_GetVersion(),enumerated,raw_open?"true":"false",(unsigned long long)(SDL_GetTicks()-begin),polls,disconnected,removed,axis_events,button_events,sensor_events);
    for(int i=0;i<axes;i++){printf("%s{\"min\":%d,\"max\":%d}",i?",":"",amin[i],amax[i]);}printf("],\"button_seen_masks\":[");
    for(int i=0;i<buttons;i++){printf("%s%u",i?",":"",bseen[i]);}printf("],\"sensors\":{");sensor_print("accelerometer",&accel,ac,ae);printf(",");sensor_print("gyro",&gyro,gc,ge);
    printf("},\"player_led_capable\":%s,\"player_index_1_request\":%s,\"player_index_2_request\":%s}\n",ledcap?"true":"false",led1?"true":"false",led2?"true":"false");
    if(pad){SDL_CloseGamepad(pad);}SDL_CloseJoystick(joy);SDL_Quit();return 0;
}
