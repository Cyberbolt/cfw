# cfw

CFW (Cyber Firewall) is a human friendly Linux firewall. (In Development)

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
curl https://raw.githubusercontent.com/Cyberbolt/cfw/main/install.py | python3
```

完成安装后，使用 `source ~/.bashrc` 激活 CFW 的环境变量。(新开 shell 将自动激活环境变量)