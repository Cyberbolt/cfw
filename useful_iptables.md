# 1. 安装
## 1.1 安装iptables之前

### 1.1.1 关闭firewalld 

`systemctl stop firewalld`

`systemctl disable firewalld`

### 1.1.2 关闭SElinux
``

## 1.2 centos

`yum install iptables`

## 1.3 ubuntu

`apt install iptables`

## 1.4 Debian

`apt install iptables`

# 2. iptables默认规则文件位置

`/etc/sysconfig/iptables`

## 2.1 保存规则文件

`service iptables save`

或

`执行命令iptables-save > xxx写入到一个文件，开机以后执行命令iptables-restore < xxx用来恢复。`

# 3. 查看所有日志
放在所有规则的前面

`iptables -I INPUT -j LOG --log-prefix "IPTables-Dropped:" --log-level 4`

## 3.1 日志等级 --log-level
- 0是emerg,
- 1是alert，
- 2是crit，
- 3是err，
- 4是warning，
- 5是notice，
- 6是info，
- 7是debug

## 3.2 日志存放位置

`/var/log/messages`


# 4. DDOS防护

## 4.1 DOS防护(单个ip访问量过大)

```python
iptables -A INPUT -i eth0 -p tcp --syn -m connlimit --connlimit-above 15 -j DROP   

iptables -A INPUT -p tcp -m state --state ESTABLISHED,RELATED -j ACCEPT  
```

## 4.2 DDOS防护

```python
iptables -A INPUT  -p tcp --syn -m limit --limit 12/s --limit-burst 24 -j ACCEPT  

iptables -A FORWARD -p tcp --syn -m limit --limit 1/s -j ACCEPT 
``` 

**ab工具模拟ddos攻击**

# 5. 配置22/ssh端口访问控制规则

## 5.1 禁止所有人

`iptables -A INPUT -p tcp --dprot 22 -j DROP`     禁止所有人访问22端口

`iptables -I INPUT -p tcp --dprot 22 -j ACCEPT`   恢复连接方法

## 5.2 禁止指定的ip

`iptables -I INPUT -s 10.0.0.1 -p tcp --dport 22 -j ACCEPT` 

# 6. 防止SYN攻击

这个方式需要调节一个合理的速度值，不然会影响正常用户的请求
```python
#使用 limit 对 syn 的每秒钟最多允许 1 个新链接，接收第三个数据包的时候触发
iptables -A INPUT -p tcp --syn -m limit --limit 1/s    --limit-burst 3 -j ACCEPT

#或者针对每个客户端做出限制，每个客户端限制并发数为 10 个，这里的十个只是为了模拟，可以自己酌情考虑
iptables -I INPUT -p tcp --syn --dport 80 -m connlimit --connlimit-above 10 -j REJECT
```

**ab工具模拟SYN攻击**

# 7. 防止 ping flooding 的发生

## 7.1 防止 ping 泛洪
```python
# 这条规则主要是防止 ping 泛洪，并且限制每秒的 ping 包不超过 10 个
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s --limit-burst 10 -j ACCEPT
```

## 自己ping别人可以  别人不能ping自己

```python
iptables -A INPUT -p icmp --icmp-type 8 -j DROP 
``` 

## 自己不能ping别人  别人可以ping自己

```python
iptables -A INPUT -p icmp --icmp-type 0 -j DROP
``` 

# 8. 防范CC攻击

## 8.1 控制单个IP的最大并发连接数

```python
iptables -I INPUT -p tcp --dport 80 -m connlimit --connlimit-above 50 -j REJECT #允许单个IP的最大连接数为 30 。
```
**默认iptables模块不包含connlimit,需要自己单独编译加载** 

## 8.2 控制单个IP在一定的时间（比如60秒）内允许新建立的连接数

```python
iptables -A INPUT -p tcp --dport 80 -m recent --name BAD_HTTP_ACCESS --update --seconds 60 --hitcount 30 -j REJECT 

iptables -A INPUT -p tcp --dport 80 -m recent --name BAD_HTTP_ACCESS --set -j ACCEPT
#单个IP在60秒内只允许最多新建30个连接。
```

# 企业级防火墙配置

## 清除防火墙规则

```python
iptables -F
iptables -X
iptables -Z
```

## 修改默认规则为拒绝（修改前先放行22端口，保证自己能够连上主机）

```python
iptables -A INPUT -p tcp --dport  22 -j ACCEPT
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP
```

## 放行指定的端口
```python
#回环允许 127.0.0.1 这个虚拟网卡上的所有网络流入和流出流量
# 设置默认规则，打开环回
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
 # 接受80， 443端口
iptables -A INPUT  -p tcp  -m multiport --dport  80,443 -j ACCEPT  

```