from typing import List

import uvicorn
from fastapi import FastAPI

import cfw

app = FastAPI()
items = []


@app.on_event("startup")
async def startup_event():
    rules, rules6 = cfw.start()
    items.append(rules)
    items.append(rules6)


"""
    ipv4
"""
@app.get("/allow_port")
def allow_port(port: str, protocol: str):
    rules, rules6 = items
    if protocol == "all":
        r_tcp = rules.add_tcp_port(port)
        r_udp = rules.add_udp_port(port)
        if not r_tcp and not r_udp:
            return {"code": 0, "message": f"{port} port tcp/udp is already open."}
    elif protocol == "tcp":
        if not rules.add_tcp_port(port):
            return {"code": 0, "message": f"{port} port tcp is already open."}
    elif protocol == "udp":
        if not rules.add_udp_port(port):
            return {"code": 0, "message": f"{port} port udp is already open."}
    rules.save_rules()
    return {"code": 1}


@app.get("/deny_port")
def deny_port(port: str, protocol: str):
    rules, rules6 = items
    if protocol == "all":
        r_tcp = rules.rm_tcp_port(port)
        r_udp = rules.rm_udp_port(port)
        if not r_tcp and not r_udp:
            return {"code": 0, "message": f"{port} port tcp/udp has been closed."}
    elif protocol == "tcp":
        if not rules.rm_tcp_port(port):
            return {"code": 0, "message": f"{port} port tcp has been closed."}
    elif protocol == "udp":
        if not rules.rm_udp_port(port):
            return {"code": 0, "message": f"{port} port udp has been closed."}
    rules.save_rules()
    return {"code": 1}


@app.get("/status")
def status_port():
    rules, rules6 = items
    ports = []
    for rule in rules.data:
        if 'tcp' in rule:
            port = (rule.split("--dport ")[1].split(" -j")[0], "tcp")
            ports.append(port)
        elif 'udp' in rule:
            port = (rule.split("--dport ")[1].split(" -j")[0], "udp")
            ports.append(port)
    ports = set(ports)
    return {"code": 1, "message": ports}


"""
    ipv6
"""
@app.get("/allow_port6")
def allow_port6(port: str, protocol: str):
    rules, rules6 = items
    if protocol == "all":
        r_tcp = rules6.add_tcp_port(port)
        r_udp = rules6.add_udp_port(port)
        if not r_tcp and not r_udp:
            return {"code": 0, "message": f"{port} port tcp/udp is already open."}
    elif protocol == "tcp":
        if not rules6.add_tcp_port(port):
            return {"code": 0, "message": f"{port} port tcp is already open."}
    elif protocol == "udp":
        if not rules6.add_udp_port(port):
            return {"code": 0, "message": f"{port} port udp is already open."}
    rules6.save_rules()
    return {"code": 1}


@app.get("/deny_port6")
def deny_port6(port: str, protocol: str):
    rules, rules6 = items
    if protocol == "all":
        r_tcp = rules6.rm_tcp_port(port)
        r_udp = rules6.rm_udp_port(port)
        if not r_tcp and not r_udp:
            return {"code": 0, "message": f"{port} port tcp/udp has been closed."}
    elif protocol == "tcp":
        if not rules6.rm_tcp_port(port):
            return {"code": 0, "message": f"{port} port tcp has been closed."}
    elif protocol == "udp":
        if not rules6.rm_udp_port(port):
            return {"code": 0, "message": f"{port} port udp has been closed."}
    rules6.save_rules()
    return {"code": 1}


@app.get("/status6")
def status_port6():
    rules, rules6 = items
    ports = []
    for rule in rules6.data:
        if 'tcp' in rule:
            port = (rule.split("--dport ")[1].split(" -j")[0], "tcp")
            ports.append(port)
        elif 'udp' in rule:
            port = (rule.split("--dport ")[1].split(" -j")[0], "udp")
            ports.append(port)
    ports = set(ports)
    return {"code": 1, "message": ports}


if __name__ == "__main__":
    uvicorn.run("server:app", port=cfw.config["port"], reload=False)
