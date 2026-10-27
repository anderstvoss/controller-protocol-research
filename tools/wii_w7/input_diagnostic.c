#define _DEFAULT_SOURCE
#include "libretro.h"
#include <stdio.h>
#include <string.h>
#include <unistd.h>
static retro_environment_t env;static retro_input_poll_t poll_input;static retro_input_state_t input;static retro_video_refresh_t video;static struct retro_sensor_interface sensor;static unsigned frame,changes[8],nonzero[8];static int16_t prev[8][20];static bool ae[8],ge[8];static unsigned gyro_nonzero[8],accel_nonzero[8];
void retro_set_environment(retro_environment_t cb){env=cb;bool yes=true;env(RETRO_ENVIRONMENT_SET_SUPPORT_NO_GAME,&yes);}
void retro_set_video_refresh(retro_video_refresh_t cb){video=cb;}
void retro_set_audio_sample(retro_audio_sample_t cb){(void)cb;}
void retro_set_audio_sample_batch(retro_audio_sample_batch_t cb){(void)cb;}
void retro_set_input_poll(retro_input_poll_t cb){poll_input=cb;}
void retro_set_input_state(retro_input_state_t cb){input=cb;}
void retro_init(void){} void retro_deinit(void){} unsigned retro_api_version(void){return RETRO_API_VERSION;}
void retro_get_system_info(struct retro_system_info*i){memset(i,0,sizeof(*i));i->library_name="W7 input-only diagnostic";i->library_version="1";i->valid_extensions="";}
void retro_get_system_av_info(struct retro_system_av_info*i){memset(i,0,sizeof(*i));i->geometry.base_width=i->geometry.max_width=2;i->geometry.base_height=i->geometry.max_height=2;i->timing.fps=50;i->timing.sample_rate=44100;}
void retro_set_controller_port_device(unsigned p,unsigned d){(void)p;(void)d;}void retro_reset(void){}
void retro_run(void){poll_input();frame++;
 if(frame==30){bool ok=env(RETRO_ENVIRONMENT_GET_SENSOR_INTERFACE,&sensor);printf("W7_SENSOR_INTERFACE %d\n",ok);for(unsigned p=0;p<8;p++){if(ok){ae[p]=sensor.set_sensor_state(p,RETRO_SENSOR_ACCELEROMETER_ENABLE,50);ge[p]=sensor.set_sensor_state(p,RETRO_SENSOR_GYROSCOPE_ENABLE,50);}}}
 for(unsigned p=0;p<8;p++){for(unsigned i=0;i<20;i++){int16_t v=i<16?input(p,RETRO_DEVICE_JOYPAD,0,i):input(p,RETRO_DEVICE_ANALOG,(i-16)/2,(i-16)%2);if(v)nonzero[p]++;if(v!=prev[p][i])changes[p]++;prev[p][i]=v;}
 if(sensor.get_sensor_input&&frame>30){for(unsigned i=0;i<3;i++){if(sensor.get_sensor_input(p,RETRO_SENSOR_GYROSCOPE_X+i)!=0)gyro_nonzero[p]++;if(sensor.get_sensor_input(p,RETRO_SENSOR_ACCELEROMETER_X+i)!=0)accel_nonzero[p]++;}}}
 static unsigned short image[4];video(image,2,2,4);usleep(20000);
 if(frame==600){for(unsigned p=0;p<8;p++)printf("W7_PORT {\"port\":%u,\"frames\":%u,\"changes\":%u,\"nonzero_controls\":%u,\"accel_enable\":%s,\"gyro_enable\":%s,\"accel_nonzero_polls\":%u,\"gyro_nonzero_polls\":%u}\n",p,frame,changes[p],nonzero[p],ae[p]?"true":"false",ge[p]?"true":"false",accel_nonzero[p],gyro_nonzero[p]);fflush(stdout);env(RETRO_ENVIRONMENT_SHUTDOWN,NULL);}}
bool retro_load_game(const struct retro_game_info*i){(void)i;return true;}bool retro_load_game_special(unsigned t,const struct retro_game_info*i,size_t n){(void)t;(void)i;(void)n;return false;}void retro_unload_game(void){}unsigned retro_get_region(void){return RETRO_REGION_NTSC;}size_t retro_serialize_size(void){return 0;}bool retro_serialize(void*d,size_t s){(void)d;(void)s;return false;}bool retro_unserialize(const void*d,size_t s){(void)d;(void)s;return false;}void retro_cheat_reset(void){}void retro_cheat_set(unsigned i,bool e,const char*c){(void)i;(void)e;(void)c;}void*retro_get_memory_data(unsigned i){(void)i;return NULL;}size_t retro_get_memory_size(unsigned i){(void)i;return 0;}
