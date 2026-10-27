#include <libudev.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
int main(int argc,char**argv){if(argc!=2)return 2;struct udev*u=udev_new();struct udev_enumerate*e=udev_enumerate_new(u);udev_enumerate_add_match_subsystem(e,"hidraw");udev_enumerate_scan_devices(e);struct udev_list_entry*p;int count=0;udev_list_entry_foreach(p,udev_enumerate_get_list_entry(e)){const char*s=udev_list_entry_get_name(p);if(strstr(s,strrchr(argv[1],'/')+1)){count++;struct udev_device*d=udev_device_new_from_syspath(u,s);udev_device_unref(d);}}
int fd=open(argv[1],O_RDWR|O_NONBLOCK);printf("owned_entries=%d owned_open=%d\n",count,fd>=0);if(fd>=0)close(fd);udev_enumerate_unref(e);udev_unref(u);return count==1&&fd>=0?0:3;}
