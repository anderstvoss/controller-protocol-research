#include <SDL3/SDL.h>
#include <SDL3/SDL_hidapi.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
int main(int argc, char **argv) {
    if (argc < 3) return 2;
    if (getenv("W2_ENABLE_WII")) {
    SDL_SetHint(SDL_HINT_JOYSTICK_HIDAPI, "1");

    }
    int raw_fd=open(argv[1],O_RDWR|O_NONBLOCK);
    printf("DIRECT_HIDRAW open=%d errno=%d\n",raw_fd>=0,raw_fd<0?errno:0);
    if(raw_fd>=0)close(raw_fd);
    if (getenv("W2_ENABLE_WII")) {
    SDL_SetHint(SDL_HINT_JOYSTICK_HIDAPI_WII, "1");
    SDL_SetHint(SDL_HINT_JOYSTICK_HIDAPI_WII_PLAYER_LED, "1");
    SDL_SetHint(SDL_HINT_JOYSTICK_ALLOW_BACKGROUND_EVENTS, "1");
    }
    printf("VERSION %d\n", SDL_GetVersion());
    if (!SDL_Init(SDL_INIT_JOYSTICK | SDL_INIT_GAMEPAD)) { printf("INIT_ERROR %s\n",SDL_GetError());return 1; }
    struct SDL_hid_device_info *devices=SDL_hid_enumerate(0x057e,0x0306);
    int raw_found=0;
    for (struct SDL_hid_device_info *d=devices;d;d=d->next) {
        if (strcmp(d->path,argv[1])==0) {
            raw_found++;
            SDL_hid_device *raw=SDL_hid_open_path(d->path);
            printf("OWNED_HID bus=%d usage_page=%u usage=%u open=%d\n",d->bus_type,d->usage_page,d->usage,raw!=NULL);
            if(raw)SDL_hid_close(raw);
        }
    }
    SDL_hid_free_enumeration(devices);
    printf("OWNED_HID_COUNT %d\n",raw_found);fflush(stdout);
    SDL_Joystick *opened[16]={0};SDL_JoystickID ids[16]={0};int total=0;
    Uint64 end=SDL_GetTicks()+12000,last=0;
    while(SDL_GetTicks()<end) {
        SDL_PumpEvents(); SDL_UpdateJoysticks();
        int count=0; SDL_JoystickID *all=SDL_GetJoysticks(&count);
        for(int i=0;i<count;i++) {
            const char *path=SDL_GetJoystickPathForID(all[i]);
            if(!path || (strcmp(path,argv[1])!=0 && strcmp(path,argv[2])!=0))continue;
            int existing=0;for(int j=0;j<total;j++)if(ids[j]==all[i])existing=1;
            if(existing || total==16)continue;
            SDL_Joystick *joy=SDL_OpenJoystick(all[i]);if(!joy){printf("OWNED_OPEN_FAILED %s\n",SDL_GetError());continue;}
            ids[total]=all[i];opened[total++]=joy;
            printf("OWNED_JOYSTICK backend=%s axes=%d buttons=%d hats=%d gamepad=%d\n",strcmp(path,argv[1])==0?"hidapi":"evdev",SDL_GetNumJoystickAxes(joy),SDL_GetNumJoystickButtons(joy),SDL_GetNumJoystickHats(joy),SDL_IsGamepad(all[i]));
            SDL_PropertiesID props=SDL_GetJoystickProperties(joy);
            printf("OUTPUT_CAPS rumble=%d player_led=%d rgb_led=%d\n",SDL_GetBooleanProperty(props,SDL_PROP_JOYSTICK_CAP_RUMBLE_BOOLEAN,false),SDL_GetBooleanProperty(props,SDL_PROP_JOYSTICK_CAP_PLAYER_LED_BOOLEAN,false),SDL_GetBooleanProperty(props,SDL_PROP_JOYSTICK_CAP_RGB_LED_BOOLEAN,false));
            printf("OUTPUT_REQUEST rumble=%d led=%d player=%d\n",SDL_RumbleJoystick(joy,0xffff,0xffff,200),SDL_SetJoystickLED(joy,1,2,3),SDL_SetJoystickPlayerIndex(joy,0));
            SDL_Gamepad *pad=SDL_OpenGamepad(all[i]);
            if(pad){printf("SENSORS accel=%d gyro=%d\n",SDL_GamepadHasSensor(pad,SDL_SENSOR_ACCEL),SDL_GamepadHasSensor(pad,SDL_SENSOR_GYRO));SDL_CloseGamepad(pad);}
        }
        SDL_free(all);
        if(SDL_GetTicks()-last>1000) {
            printf("SNAPSHOT owned_count=%d",total);
            for(int i=0;i<total;i++)printf(" connected%d=%d axes%d=%d buttons%d=%d",i,SDL_JoystickConnected(opened[i]),i,SDL_GetNumJoystickAxes(opened[i]),i,SDL_GetNumJoystickButtons(opened[i]));
            printf("\n");fflush(stdout);last=SDL_GetTicks();
        }
        SDL_Event event;while(SDL_PollEvent(&event)){}
        SDL_Delay(5);
    }
    for(int i=0;i<total;i++)SDL_CloseJoystick(opened[i]);
    SDL_Quit();return 0;
}
