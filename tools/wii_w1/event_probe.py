import array, fcntl, json, os, select, struct, sys, time
nodes=[]
for path in sys.argv[1:]:
    node={'role_index':len(nodes),'opened':False,'axes':[],'events':[]}
    try:
        fd=os.open(path,os.O_RDONLY|os.O_NONBLOCK)
        node['opened']=True
        mask=array.array('B',[0]*8)
        fcntl.ioctl(fd,0x80084523,mask,True)
        for code in range(64):
            if mask[code//8] & (1<<(code%8)):
                values=array.array('i',[0]*6)
                fcntl.ioctl(fd,0x80184540+code,values,True)
                node['axes'].append(dict(zip(['value','minimum','maximum','fuzz','flat','resolution'],values),code=code))
        node['fd']=fd
    except OSError as error:
        node['errno']=error.errno
    nodes.append(node)
print('READY',flush=True)
end=time.monotonic()+2
while time.monotonic()<end:
    ready,_,_=select.select([n['fd'] for n in nodes if 'fd' in n],[],[],0.02)
    for node in nodes:
        if node.get('fd') in ready:
            try:
                data=os.read(node['fd'],24*256)
                for _,_,kind,code,value in struct.iter_unpack('llHHi',data):
                    event=[kind,code,value]
                    if kind in (0,1,3) and event not in node['events']:
                        node['events'].append(event)
            except OSError as error:
                node['read_errno']=error.errno
for node in nodes:
    if 'fd' in node:
        fd=node.pop('fd')
        for axis in node['axes']:
            values=array.array('i',[0]*6)
            fcntl.ioctl(fd,0x80184540+axis['code'],values,True)
            axis['delivered_value']=values[0]
        os.close(fd)
print(json.dumps(nodes))
