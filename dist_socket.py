#!coding=utf-8

import threading
import socket
import struct
import sys
import os
import time
from typing import Any, Optional, Sequence, Tuple, Union, List
from backend_tools import inference_trt

class father_point:

    def __init__(
        self,
        son_ip_list: Optional[List] = None,
        son_port_list: Optional[List] = None,
        son_name_list: Optional[List] = None,
        src: Optional[str] = None, 
        dst: Optional[str] = None
    ) -> None:
        
        self.son_ip_list = son_ip_list
        self.son_port_list = son_port_list
        self.son_name_list = son_name_list
        self.src = src
        self.dst = dst

        ssh_list = []
        assert len(son_ip_list) > 0 , 'check your ip list'
        print("-"*70)
        for i in range(len(son_ip_list)):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((son_ip_list[i], son_port_list[i]))
                #print(s,type(s))
            except socket.error as msg:
                print(msg)
                sys.exit(1)
            print(s.recv(1024).decode('utf-8'))
            ssh_list.append(s)
        self.ssh_list = ssh_list
        
    
    def father_sending_order(self,order):
        
        print("-"*70)
        print('asking for {0} operation ~'.format(order))

        if order in ['broadcast','scatter','inference','quit']:
            for s in self.ssh_list:
                s.send('asking for {0} operation ~'.format(order).encode('utf-8'))
                time.sleep(0.5)
                print(s.recv(1024).decode('utf-8'))
        
            if order == 'broadcast' : 
                self.father_broadcast()
            
            elif order == 'scatter' : 
                self.father_scatter()
            
            elif order == 'inference':
                self.father_inference()
            
            elif order == 'quit' :
                self.father_quit()

        elif order in ['gather']:
            for s in self.ssh_list:
                s.send('asking for {0} operation ~'.format(order).encode('utf-8'))
                print(s.recv(1024).decode('utf-8'))
                
                if order == 'gather':
                    self.father_gather(s)


    def father_broadcast(self):
        file_lists = [[] for _ in range(len(self.ssh_list))]

        if os.path.isdir(self.src):
            
            print("-"*70)
            print("extract data from",self.src)

            for imgs in os.listdir(self.src):
                file_extension = imgs.split(".")[-1]
                image_extensions = get_image_extension()
        
                if file_extension in image_extensions:
                    filepath = os.path.join(self.src,imgs)
                    for i in range(len(self.ssh_list)):
                         file_lists[i].append(filepath)
                else:
                    pass
        else:
            pass

        for s in self.ssh_list:
            s.send(os.path.abspath(self.src).split("\\")[-1].encode('utf-8'))
            time.sleep(0.1)
            file_client(file_lists[self.ssh_list.index(s)],s,self.son_name_list[self.ssh_list.index(s)],1)
    
    def father_scatter(self):
        file_lists = [[] for _ in range(len(self.ssh_list))]
        div_count = 0
        if os.path.isdir(self.src):
            
            print("-"*70)
            print("extract data from",self.src)

            for imgs in os.listdir(self.src):
                file_extension = imgs.split(".")[-1]
                image_extensions = get_image_extension()

                if file_extension in image_extensions:
                    filepath = os.path.join(self.src,imgs)
                    file_lists[div_count%len(self.ssh_list)].append(filepath)
                    div_count += 1
                else:
                    pass
        else:
            pass

        for s in self.ssh_list:
            s.send(os.path.abspath(self.src).split("\\")[-1].encode('utf-8'))
            time.sleep(0.1)
            file_client(file_lists[self.ssh_list.index(s)],s,self.son_name_list[self.ssh_list.index(s)],1)

    def father_inference(self):
        if os.path.isdir(self.src):
            for files in os.listdir(self.src):
                if files.split(".")[0] == 'config':
                    
                    print("-"*70)
                    print("extract configs from",os.path.join(self.src,files),":")
                    user, mode, model, data, backbone, cropsize, quant = get_configs(os.path.join(self.src,files))
                    self.user = user
                    print(user, mode, model, data, backbone, cropsize, quant)
                    src = os.path.abspath(self.src).split("\\")[-1]
                    configs_patch1 = struct.pack('64s64s',user.encode('utf-8'), mode.encode('utf-8'))
                    configs_patch2 = struct.pack('64s64s',model.encode('utf-8'), data.encode('utf-8'))
                    configs_patch3 = struct.pack('64s64s',backbone.encode('utf-8'), cropsize.encode('utf-8'))
                    configs_patch4 = struct.pack('64s64s',quant.encode('utf-8'), src.encode('utf-8'))

        for s in self.ssh_list:
            s.send(configs_patch1)
            s.send(configs_patch2)
            s.send(configs_patch3)
            s.send(configs_patch4)
            #time.sleep(0.1)
        
        for s in self.ssh_list:
            print(s.recv(1024).decode('utf-8'))

    def father_gather(self,s):
        
        print("-"*70)
        print('start processing gather')
        foldername = s.recv(1024).decode('utf-8')
        os.makedirs(os.path.join(self.dst,foldername),exist_ok=True)
        file_server(os.path.join(self.dst,foldername),s,'128si')

    def father_quit(self):
        
        print("-"*70)
        for s in self.ssh_list:
            print('{0} shut down !'.format(self.son_name_list[self.ssh_list.index(s)]))
            s.close()



class son_point:

    def __init__(
        self,
        ip: Optional[str] = None,
        port: Optional[int] = None,
        name: Optional[str] = None,
        src: Optional[str] = None, #source images folder
        dst: Optional[str] = None
    ) -> None:
        
        self.ip = ip
        self.port = port
        self.name = name
        self.src = src
        self.dst = dst

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.ip, self.port))
            s.listen(5)
        except socket.error as msg:
            print(msg)
            sys.exit(1)
        self.sockinfo = s
        self.son_connect()

    def son_connect(self):
        print("-"*70)
        print('Waiting connection...')

        conn, addr = self.sockinfo.accept()
        t = threading.Thread(target=son_deal_connect, args=(conn, addr, self.name))
        t.start()
        self.son_waiting_order(conn)

    def son_waiting_order(self,conn):
        
        print("-"*70)
        print('Waiting order...')
        order = conn.recv(1024).decode('utf-8').split(" ")[2]
        conn.send('{0} is ready for {1} operation !'.format(self.name,order).encode('utf-8'))
        print('{0} is ready for {1} operation !'.format(self.name,order))
        
        if order == 'broadcast' : 
            self.son_broadcast(conn)
        
        elif order == 'scatter' : 
            self.son_scatter(conn)

        elif order == 'inference' : 
            self.son_inference(conn)
        
        elif order == 'gather' : 
            self.son_gather(conn)
        
        elif order == 'quit' :
            self.son_quit(conn)
    
    def son_broadcast(self,conn):
        
        print("-"*70)
        print('start processing broadcast')
        foldername = conn.recv(1024).decode('utf-8')
        self.foldername = foldername
        os.makedirs(os.path.join(self.dst,foldername),exist_ok=True)
        file_server(os.path.join(self.dst,foldername),conn,'128si')
        self.son_waiting_order(conn)
    
    def son_scatter(self,conn):
        
        print("-"*70)
        print('start processing scatter')
        foldername = conn.recv(1024).decode('utf-8')
        self.foldername = foldername
        os.makedirs(os.path.join(self.dst,foldername),exist_ok=True)
        file_server(os.path.join(self.dst,foldername),conn,'128si')
        self.son_waiting_order(conn)
    
    def son_inference(self,conn):
        
        print("-"*70)
        print('start processing inference')
        config_size = struct.calcsize('64s64s')
        buf1 = conn.recv(config_size)
        buf2 = conn.recv(config_size)
        buf3 = conn.recv(config_size)
        buf4 = conn.recv(config_size)
        user, mode = struct.unpack('64s64s', buf1)
        model, data = struct.unpack('64s64s', buf2)
        backbone, cropsize = struct.unpack('64s64s', buf3)
        quant, src = struct.unpack('64s64s', buf4)
        user = user.strip(b'\00').decode('utf-8')
        mode = mode.strip(b'\00').decode('utf-8')
        model = model.strip(b'\00').decode('utf-8')
        data = data.strip(b'\00').decode('utf-8')
        backbone = backbone.strip(b'\00').decode('utf-8')
        cropsize = cropsize.strip(b'\00').decode('utf-8')
        quant = quant.strip(b'\00').decode('utf-8')
        src = src.strip(b'\00').decode('utf-8')
        self.user = user
        print(user, mode, model, data, backbone, cropsize, quant,src)
        
        inference_trt(
        mode = mode,
        cropsize = cropsize,
        quant = quant,
        model = model,
        data = data,
        backbone = backbone,
        user = user,
        src = src,
        workdirs='./',)

        conn.send('{0} inference complete!'.format(self.name).encode('utf-8'))
        print('{0} inference complete!'.format(self.name))
    
        self.son_waiting_order(conn)

    def son_gather(self,conn):
        
        print("-"*70)
        print('start processing gather')
        dst_dir = os.path.join(self.src,self.user+"-"+self.foldername)
        if os.path.isdir(dst_dir):
            print("extract data from",dst_dir)
            file_list = []
            for imgs in os.listdir(dst_dir):
                file_extension = imgs.split(".")[-1]
                image_extensions = get_image_extension()
        
                if file_extension in image_extensions:
                    filepath = os.path.join(dst_dir,imgs)
                    file_list.append(filepath)
                else:
                    pass
        
        conn.send((self.user+"-"+self.foldername).encode('utf-8'))
        time.sleep(0.1)
        file_client(file_list,conn,"fatherpoint",1)
        self.son_waiting_order(conn)

    def son_quit(self,conn):
        
        print("-"*70)
        print('start processing quit')
        conn.close()
        self.son_connect()

def son_deal_connect(conn, addr, name):
    print('Accept new connection from {0}\n'.format(addr))
    conn.send('Hi, Welcome to {0} server!'.format(name).encode('utf-8'))

def file_client(file_list:List,s,name:str,interval:float = 1,pack_type:str = '128si'):
    """
    send files in file_list through s to IP name
    interval is suggested to be set to 1

    Args:
        file_list: 文件地址列表
        s: socket连接
        name: 连接IP的昵称
        interval: 传输间隔时间,建议设置为1
        pack_type: 压缩包时的数据类型
    """

    for filepath in file_list:
        fhead = struct.pack(pack_type, os.path.basename(filepath).encode('utf-8'), os.stat(filepath).st_size)
        gap_count = 0
        s.send(fhead)
        time.sleep(0.1)
        t1 = time.time()
        fp = open(filepath, 'rb')
        while 1:
            data = fp.read(1024)
            if not data:
                t2 = time.time()
                print('{:>12s} sends over to {:>10s}, upload speed: {:.3f} Mbps'.format(os.path.basename(filepath),name,1.0*os.stat(filepath).st_size/(t2-t1)/1024/1024))
                break
            s.send(data)
            gap_count += 1

            # 模拟真实的网络延迟
            if(gap_count % 10 == 0) :
                time.sleep(0.015)
    
        time.sleep(interval)

    fhead = struct.pack(pack_type, "finish broadcast!".encode('utf-8'), 0)
    s.send(fhead)

def file_server(folder_path,conn,unpack_type:str = '128si'):
    """
    accept files through conn

    Args:
        folder_path: 存放文件的文件夹地址
        conn: socket连接
        unpack_type: 解包时的数据类型
    """
    while 1:
        fileinfo_size = struct.calcsize(unpack_type)
        buf = conn.recv(fileinfo_size)
            
        filename, filesize = struct.unpack(unpack_type, buf)
        fn = filename.strip(b'\00').decode('utf-8')
        if filesize > 0:
            t1 = time.time()
            recvd_size = 0
            fp = open(os.path.join(folder_path,fn), 'wb')

            while not recvd_size >= filesize:
                data = conn.recv(1024)
                recvd_size += len(data)
                fp.write(data)
            fp.close()

            t2 = time.time()
            print('    accepting {:10s}, filesize is {:>10d}, download speed: {:.3f} Mbps'.format(str(fn), filesize,1.0*filesize/(t2-t1)/1024/1024))
            
        else:
            print(fn)
            break

def get_image_extension():
    image_extensions = ['jpg','jpeg','png','gif']
    return image_extensions

def get_configs(path):
    with open(path,'r') as f:
        user = f.readline().strip()
        mode = f.readline().strip()
        model = f.readline().strip()
        data = f.readline().strip()
        backbone = f.readline().strip()
        cropsize = f.readline().strip()
        quant = f.readline().strip()
    return user, mode, model, data, backbone, cropsize, quant