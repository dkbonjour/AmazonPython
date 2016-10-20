# 服务器行为准则

所有服务器都是Centos,所以准则如下：

## 基本命令
```
df -h 查看磁盘
free -h 查看内存
ip -s addr 查看ip地址
ifconfig 
```

## 规范

(1)：文件结构

```
mkdir /data
cd /data
app -> /usr/local
ln -s /usr/local app
```

建立/data/app (放安装软件)

建立/data/www (放运行程序)

(2):日常操作

设置环境变量：

```
cd /etc/profile.d
vim myenv.sh
source myenv.sh
```

更改host
```
vim /etc/hosts
```

## 维护

磁盘扩容
http://www.centoscn.com/CentOS/config/2015/0315/4891.html

```
centos7安装后，磁盘分了3个逻辑卷，
/dev/centos/root
/dev/centos/swap
/dev/centos/home
大部分磁盘空间都分给home了。
现在希望把空间分给root。

以下命令，通过system-storage-manager，删除home分区，把空间增加到root里。

（由于新装的系统，home下是空的，可以直接删除。
而且，由于home的文件系统是xfs，似乎只能扩容不支持缩减，所以只好删除。）


# 安装ssm
yum --disablerepo=* --enablerepo=ustc* install system-storage-manager

# 查看分区
ssm list

# 卸载home
umount /home

# 删除逻辑卷home
ssm remove /dev/centos/home

# 查看释放出来的空间，并增加到root上
ssm list
ssm resize -s +1.76T /dev/centos/root

# 还需要使用xfs_growfs扩容文件系统
ssm list
xfs_growfs /dev/centos/root

# 最后，要把fstab中挂载home的一行删掉
vi /etc/fstab

```

网路设置

ping 一个外网ip，比如114.114.114.114 看下通不，通的话就是dns的问题，ping不通那就是网关的问题

http://www.cnblogs.com/visi_zhangyang/articles/2429185.html

```
CentOS修改IP地址

# ifconfig eth0 192.168.1.80

这样就把IP地址修改为192.168.1.80(如果发现上不了网了，那么你可能需要把网关和DNS也改一下，后面会提到)，但是当你重新启动系统或网卡之后，还是会变回原来的地址，这种修改方式只适用于需要临时做IP修改。要想永久性修改，就要修改/etc/sysconfig/network-scripts/ifcfg-eth0这个文件，这个文件的主要内容如下（你的文件中没有的项，你可以手动添加）：

# vi  /etc/sysconfig/network-scripts/ifcfg-eth0

DEVICE=eth0 #描述网卡对应的设备别名

BOOTPROTO=static #设置网卡获得ip地址的方式，选项可以为为static，dhcp或bootp

BROADCAST=192.168.1.255 #对应的子网广播地址

HWADDR=00:07:E9:05:E8:B4 #对应的网卡物理地址

IPADDR=12.168.1.80 #只有网卡设置成static时，才需要此字段

NETMASK=255.255.255.0 #网卡对应的网络掩码

NETWORK=192.168.1.0 #网卡对应的网络地址，也就是所属的网段

ONBOOT=yes #系统启动时是否设置此网络接口，设置为yes时，系统启动时激活此设备

 

 

CentOS修改网关

# route add default gw 192.168.1.1 dev eth0

这样就把网关修改为192.168.1.1了，这种修改只是临时的，当你重新启动系统或网卡之后，还是会变回原来的网关。要想永久性修改，就要修改/etc/sysconfig/network 这个文件，这个文件的主要内容如下（你的文件中没有的项，你可以手动添加）：

# vi  /etc/sysconfig/network

NETWORKING=yes #表示系统是否使用网络，一般设置为yes。如果设为no，则不能使用网络。

HOSTNAME=centos #设置本机的主机名，这里设置的主机名要和/etc/hosts中设置的主机名对应

GATEWAY=192.168.1.1 #设置本机连接的网关的IP地址。

**********上面的文件修改完要重新启动一下网卡才会生效：# service network restart ********

CentOS修改DNS

上面的都修改完之后，当你ping一个域名是肯能不通，但ping对应的IP地址是同的，这时我们需要修改一下DNS。修改DNS要通过修改/etc/resolv.conf这个文件：

# vi /etc/resolv.conf

nameserver 8.8.8.8 #google域名服务器 nameserver 8.8.4.4 #google域名服务器

通过上面的所有设置，系统应该可以上网了。

如果centos系统建立在虚拟机之上，那么在设置虚拟机的网络时请选择‘网桥适配器’连接。
```