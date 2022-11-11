# cfw

[中文版](https://github.com/Cyberbolt/cfw#%E4%B8%AD%E6%96%87%E7%89%88)

CFW (Cyber Firewall) is a human friendly Linux firewall. (In Development) It is designed to help prevent denial of service attacks while controlling Linux port switches.

The software is based on iptables and ipset and is developed with Python. It is recommended to close the firewall (such as firewalld, ufw) that comes with the distribution to avoid conflicts.

With CFW, you will be able to:

- Automatically block malicious IPs in the Internet through custom rules to prevent denial of service attacks

- Control to open or close the Linux TCP/UDP port

- Get a friendly interactive experience

To use with CDN, please set the ip segment of CDN to CFW whitelist.

### Implementation

CFW gets all connections to the current server with the `ss -Hntu | awk '{print $5,$6}'` command. If the client's request exceeds the set concurrent number, the ip will be blocked by iptables and stored in the ipset data structure.

CFW implements Linux port switching by invoking the iptables command.

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

### uninstallation

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

#### run

Stop CFW `systemctl stop cfw`

Start CFW `systemctl start cfw`

Restart CFW `systemctl restart cfw`

#### ip blacklist management

Manually block a single ipv4 `cfw block [ip]`

Manually unblock a single ipv4 `cfw unblock [ip]`

View ipv4 blacklist `cfw blacklist`

Manually block a single ipv6 `cfw block6 [ip]`

Manually unblock a single ipv6 `cfw unblock6 [ip]`

View ipv6 blacklist `cfw blacklist6`

#### Linux port operation

Allow ipv4 port `cfw allow [port]`

Block ipv4 ports `cfw deny [port]`

Separately allow ipv4 TCP port `cfw allow [port]/tcp`, for example `cfw allow 69.162.81.155/tcp`

Block ipv4 TCP ports individually `cfw deny [port]/tcp`, e.g. `cfw deny 69.162.81.155/tcp`

ipv4 UDP port operation is the same

View all allowed ipv4 ports `cfw status`

Allow ipv6 port `cfw allow6 [port]`

Block ipv6 port `cfw deny6 [port]`

Separately allow ipv6 TCP port `cfw allow6 [port]/tcp`, for example `cfw allow6 69.162.81.155/tcp`

Block ipv6 TCP ports individually `cfw deny6 [port]/tcp`, e.g. `cfw deny6 69.162.81.155/tcp`

ipv6 UDP port operation is the same

View all allowed ipv6 ports `cfw status6`

#### log operations

Dynamic query log `cfw log [num]`. 'num' is the number of query logs, and the query results will be in reverse chronological order.

### More

If you encounter any problems in use, please leave a message at [https://github.com/Cyberbolt/cfw/issues](https://github.com/Cyberbolt/cfw/issues).

# 中文版

CFW (Cyber Firewall) 是一个人性化的 Linux 防火墙。它旨在协助阻止拒绝服务攻击，同时能控制 Linux 端口开关。

该软件基于 iptables 和 ipset，使用 Python 开发，使用时建议关闭发行版自带的防火墙(如 firewalld、ufw)避免冲突。

通过 CFW，您将能够：

- 通过自定义的规则自动封禁互联网中的恶意 ip，以防止拒绝服务攻击

- 控制开启或关闭 Linux 的 TCP/UDP 端口

- 获得友好的交互式体验

如欲配合 CDN 使用，请将 CDN 的 ip 段设置为 CFW 白名单。

### 实现方法

CFW 通过 `ss -Hntu | awk '{print $5,$6}'` 命令获取当前服务器的所有连接。客户端的请求若超过设定并发数，该 ip 将被 iptables 封禁，并存储在 ipset 数据结构中。

CFW 通过调用 iptables 命令实现 Linux 端口开关。

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