# CFW

[中文版](https://github.com/Cyberbolt/cfw#%E4%B8%AD%E6%96%87%E7%89%88)

CFW (Cyber Firewall) is a human friendly Linux firewall. It is designed to help prevent denial-of-service attacks (DDOS), and can control the opening and closing of Linux system ports. Since it runs natively based on Linux, CFW has good software compatibility.

The software is based on iptables and ipset, and is developed in Python. When using it, it is recommended to turn off the firewall (such as firewalld, ufw) that comes with the distribution to avoid conflicts.

With CFW you will be able to:

- Automatically block malicious ip in the Internet through custom rules to prevent denial of service attacks

- Protects all ports of Linux from DDOS attacks, not just web applications

- Obtain good software compatibility, natively support Nginx, Caddy and other servers

- Supports the use of CDN, when using CDN, please set the ip segment of CDN to CFW whitelist

- Control open or close the TCP/UDP port of the Linux system

- Get a friendly command-line interactive experience

### Background

Web applications run on the complex Internet and may face malicious attacks at any time, resulting in denial of service. To ban these unfriendly ip, CFW was born for this.

CFW was originally inspired by Pagoda Panel's Nginx Firewall. However, I encountered many difficulties in the process of using the Nginx firewall. The firewall only protects against CC attacks against web applications (usually ports 80 and 443), and cannot protect other ports of Linux servers. At the same time, the firewall needs to be paid on a monthly basis, and it is always bundled with the pagoda ecology (the latest pagoda panel even needs to log in to an account bound to the real-name system of the mobile phone), thus limiting the degree of freedom of the software. We wanted to run a firewall on all ports in clean Linux, so we developed one ourselves.

Since CFW is based on iptables and ipset, it will inevitably conflict with the firewall (such as firewalld, ufw) that comes with the distribution. We have added CFW to control the port switch.

### Implementation

CFW gets all the connections of the current server through `ss -Hntu | awk '{print $5,$6}'` command. If the client's request exceeds the set concurrent number, the ip will be blocked by iptables and stored in the ipset data structure.

CFW realizes the switch of Linux port by calling iptables command.

### Installation

Please make sure that the system has the following dependencies:

Example 1 (Debian, Ubuntu)

```
apt install -y curl ipset python3 git net-tools
```

Example 2 (CentOS)

```
yum install -y curl ipset python3 git net-tools
```

After installing the system dependencies, enter the following command to install CFW:

```
sudo curl https://raw.githubusercontent.com/Cyberbolt/cfw/main/install.py | python3
```

Once installed, use `source ~/.bashrc` to activate CFW's environment variables. (A new shell will automatically activate the environment variable)

Enter `systemctl status cfw` in the Linux terminal, if `active (running)` is displayed, it means that CFW has been successfully run, and it will run automatically when the server restarts.

### Uninstallation

```
sudo curl https://raw.githubusercontent.com/Cyberbolt/cfw/main/uninstall.py | python3
```

### Links

- GitHub: https://github.com/Cyberbolt/cfw
- CyberLight: https://www.cyberlight.xyz/
- Potato Blog: https://www.liuya.love/

### Configuration

The configuration file is in `/etc/cfw/config.yaml`. After modifying the configuration file, run `systemctl restart cfw` to take effect.

Configuration file parameter description:
```
# CFW running port
port: 6680
# The frequency at which CFW detects connections, in seconds. The 
# default here is every 5 seconds.
frequency: 5
# The maximum number of concurrent connections per ip is allowed. 
# Exceeding it will be banned by CFW.
max_num: 100
# The time to unblock the ip. The default ip here will be automatically 
# unblocked 600 seconds after it is blocked. If the value here is 0, 
# it will be permanently banned.
unblock_time: 600
# Data backup time, unit: seconds.
backup_time: 60

# ipv4 whitelist path. Written in txt, one ip per line, supports 
# subnet mask. (The local address and intranet address are in this 
# file by default)
whitelist: /etc/cfw/ip_list/whitelist.txt
# ipv4 blacklist path. Written in txt, one ip per line, supports 
# subnet mask.
blacklist: /etc/cfw/ip_list/blacklist.txt

# ipv6 whitelist path. Written in txt, one ip per line.
whitelist6: /etc/cfw/ip_list/whitelist6.txt
# ipv6 blacklist path. Written in txt, one ip per line.
blacklist6: /etc/cfw/ip_list/blacklist6.txt

# path to log file
log_file_path: /etc/cfw/log/log.csv
# The maximum number of lines in the log file. (It will scroll 
# automatically after reaching the maximum number of rows. If 
# the value here is 0, the maximum number of rows is not limited)
log_max_lines: 10000000
```

### Related commands

All `[]` in the command represent variables.

#### Run

Stop CFW `systemctl stop cfw`

Start CFW `systemctl start cfw`

Restart CFW `systemctl restart cfw`

#### Ip Blacklist Management

Manually block a single ipv4 `cfw block [ip]`

Manually unblock a single ipv4 `cfw unblock [ip]`

View ipv4 blacklist `cfw blacklist`

Manually block a single ipv6 `cfw block6 [ip]`

Manually unblock a single ipv6 `cfw unblock6 [ip]`

View ipv6 blacklist `cfw blacklist6`

#### Linux port operation

Allow ipv4 port `cfw allow [port]`

Block ipv4 port `cfw deny [port]`

Separately allow ipv4 TCP port `cfw allow [port]/tcp`, for example `cfw allow 69.162.81.155/tcp`

Block ipv4 TCP port individually `cfw deny [port]/tcp`, e.g. `cfw deny 69.162.81.155/tcp`

ipv4 UDP port operation is the same

View all allowed ipv4 ports `cfw status`

Allow ipv6 port `cfw allow6 [port]`

Block ipv6 port `cfw deny6 [port]`

Separately allow ipv6 TCP port `cfw allow6 [port]/tcp`, for example `cfw allow6 69.162.81.155/tcp`

Block ipv6 TCP port individually `cfw deny6 [port]/tcp`, e.g. `cfw deny6 69.162.81.155/tcp`

ipv6 UDP port operation is the same

View all allowed ipv6 ports `cfw status6`

#### Log Operations

Dynamic query log `cfw log [num]`. 'num' is the number of query logs, and the query results will be in reverse chronological order.

### More

If you encounter any problems in use, please leave a message at [https://github.com/Cyberbolt/cfw/issues](https://github.com/Cyberbolt/cfw/issues).

# 中文版

CFW (Cyber Firewall) 是一个人性化的 Linux 防火墙。它旨在协助阻止拒绝服务攻击 (DDOS)，同时能控制 Linux 系统端口的开关。由于基于 Linux 原生运行，CFW 拥有良好的软件兼容性。

该软件基于 iptables 和 ipset，使用 Python 开发，使用时建议关闭发行版自带的防火墙 (如 firewalld、ufw) 避免冲突。

通过 CFW，您将能够：

- 通过自定义的规则自动封禁互联网中的恶意 ip，以防止拒绝服务攻击

- 保护 Linux 的所有端口遭受 DDOS 攻击，而不仅仅是 Web 应用

- 获得良好的软件兼容性，原生支持 Nginx、Caddy 等服务器

- 支持配合 CDN 使用，使用 CDN 时请将 CDN 的 ip 段设置为 CFW 白名单

- 控制开启或关闭 Linux 系统的 TCP/UDP 端口

- 获得友好的命令行交互式体验

### 项目背景

Web 应用程序运行在复杂的互联网中，随时可能面临恶意攻击，导致拒绝服务现象。封禁这些不友好的 ip，CFW 正是为此而诞生。

CFW 的灵感最初来自宝塔面板的 Nginx 防火墙。然而，使用 Nginx 防火墙的过程中遇到诸多不顺。该防火墙仅针对 Web 应用 (通常是 80 和 443 端口) 防御 CC 攻击，无法保护 Linux 服务器的其他端口。同时，该防火墙需要按月付费，并始终捆绑宝塔生态(最新的宝塔面板甚至需要登录绑定手机实名制的账号)，从而限制了软件自由度。我们想在纯净的 Linux 中运行防火墙，并对所有端口生效，于是自己开发了一个。

由于 CFW 基于 iptables 和 ipset，不免会与发行版自带的防火墙 (如 firewalld、ufw) 冲突，我们增加了 CFW 对端口开关的控制。

### 实现方法

CFW 通过 `ss -Hntu | awk '{print $5,$6}'` 命令获取当前服务器的所有连接。客户端的请求若超过设定并发数，该 ip 将被 iptables 封禁，并存储在 ipset 数据结构中。

CFW 通过调用 iptables 命令实现 Linux 端口的开关。

### 安装

请先确保系统拥有以下依赖：

示例 1 (Debian, Ubuntu)

```
apt install -y curl ipset python3 git net-tools
```

示例 2 (CentOS)

```
yum install -y curl ipset python3 git net-tools
```

安装好系统依赖后，输入以下命令安装 CFW：

```
sudo curl https://raw.githubusercontent.com/Cyberbolt/cfw/main/install.py | python3
```

完成安装后，使用 `source ~/.bashrc` 激活 CFW 的环境变量。(新开 shell 将自动激活环境变量)

在 Linux 终端输入 `systemctl status cfw`，显示 `active (running)` 字样说明 CFW 已成功运行，同时会在服务器重启时自动运行。

### 卸载

```
sudo curl https://raw.githubusercontent.com/Cyberbolt/cfw/main/uninstall.py | python3
```

### 链接

- GitHub: https://github.com/Cyberbolt/cfw
- 电光笔记: https://www.cyberlight.xyz/
- Potato Blog: https://www.liuya.love/

### 配置

配置文件在 `/etc/cfw/config.yaml` 中，修改配置文件后运行 `systemctl restart cfw` 即可生效。

配置文件参数说明：
```
# CFW 运行端口
port: 6680
# CFW 检测连接的频率，单位：秒。此处默认 5 秒一次。
frequency: 5
# 允许每个 ip 连接的最大并发数，超过将被 CFW 封禁。
max_num: 100
# 解封 ip 的时间。此处默认 ip 被封禁后 600 秒将自动解封。若此处值为 0，则永久封禁。
unblock_time: 600
# 数据备份时间，单位：秒。
backup_time: 60

# ipv4 白名单路径。写在 txt 中，一行一个 ip，支持子网掩码。(本地地址、内网地址默认在该文件中)
whitelist: /etc/cfw/ip_list/whitelist.txt
# ipv4 黑名单路径。写在 txt 中，一行一个 ip，支持子网掩码。
blacklist: /etc/cfw/ip_list/blacklist.txt

# ipv6 白名单路径。写在 txt 中，一行一个 ip。
whitelist6: /etc/cfw/ip_list/whitelist6.txt
# ipv6 黑名单路径。写在 txt 中，一行一个 ip。
blacklist6: /etc/cfw/ip_list/blacklist6.txt

# 日志文件的路径
log_file_path: /etc/cfw/log/log.csv
# 日志文件的最大行数。（达到最大行数后将自动滚动。若此处值为 0，则不限制最大行数）
log_max_lines: 10000000
```

### 相关命令

命令中所有 `[]` 表示变量。

#### 运行

停止 CFW `systemctl stop cfw`

启动 CFW `systemctl start cfw`

重启 CFW `systemctl restart cfw`

#### ip 黑名单管理

手动封禁单个 ipv4 `cfw block [ip]`

手动解封单个 ipv4 `cfw unblock [ip]`

查看 ipv4 黑名单 `cfw blacklist`

手动封禁单个 ipv6 `cfw block6 [ip]`

手动解封单个 ipv6 `cfw unblock6 [ip]`

查看 ipv6 黑名单 `cfw blacklist6`

#### Linux 端口操作

放行 ipv4 端口 `cfw allow [port]`

阻止 ipv4 端口 `cfw deny [port]`

单独放行 ipv4 TCP 端口 `cfw allow [port]/tcp`，示例如 `cfw allow 69.162.81.155/tcp`

单独阻止 ipv4 TCP 端口 `cfw deny [port]/tcp`，示例如 `cfw deny 69.162.81.155/tcp`

ipv4 UDP 端口操作同理

查看所有放行的 ipv4 端口 `cfw status`

放行 ipv6 端口 `cfw allow6 [port]`

阻止 ipv6 端口 `cfw deny6 [port]`

单独放行 ipv6 TCP 端口 `cfw allow6 [port]/tcp`，示例如 `cfw allow6 69.162.81.155/tcp`

单独阻止 ipv6 TCP 端口 `cfw deny6 [port]/tcp`，示例如 `cfw deny6 69.162.81.155/tcp`

ipv6 UDP 端口操作同理

查看所有放行的 ipv6 端口 `cfw status6`

#### 日志操作

动态查询日志 `cfw log [num]`。'num' 为查询日志的条数，查询结果将按时间倒序。

### 更多

如果您在使用中遇到任何问题，欢迎在 [https://github.com/Cyberbolt/cfw/issues](https://github.com/Cyberbolt/cfw/issues) 处留言。