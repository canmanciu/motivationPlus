

def getip(request):
    # 尝试从 X-Forwarded-For 头获取 IP 地址
    ip_address = request.headers.getlist("X-Forwarded-For", type=str)
    if ip_address:
        # 如果存在多个 IP（通过逗号分隔），通常第一个 IP 是客户端的 IP
        client_ip = ip_address[0]
    else:
        # 如果 X-Forwarded-For 头不存在，使用 remote_addr
        client_ip = request.remote_addr

    return client_ip

