import uvicorn

from fastapi import FastAPI

import cfw

app = FastAPI()


@app.get("/allow_port")
def allow_port(port: str, protocol: str):
    if protocol == "all":
        r_tcp = cfw.rules.add_tcp_port(port)
        r_udp = cfw.rules.add_udp_port(port)
        if not r_tcp and not r_udp:
            return {"code": 0, "message": f"{port} port tcp/udp is already open."}
    elif protocol == "tcp":
        if not cfw.rules.add_tcp_port(port):
            return {"code": 0, "message": f"{port} port tcp is already open."}
    elif protocol == "udp":
        if not cfw.rules.add_udp_port(port):
            return {"code": 0, "message": f"{port} port udp is already open."}
    cfw.rules.save_rules()
    return {"code": 1}


@app.get("/deny_port")
def deny_port(port: int):
    cfw.rules.rm_tcp_port(port)
    return {"code": 1}


@app.get("/deny_tcp_port")
def allow_delete_udp_port(port: int):
    cfw.rules.add_udp_port(port)
    return {"code": 1}


if __name__ == "__main__":
    cfw.start()
    uvicorn.run("server:app", port=cfw.config["port"])
