# Author pengzihao
# Date 2019/1/4
import socket
import platform
import threading

open_num = 0
lock = threading.Lock()


def tcp_connect(ip, port_number, delay_time, open_port):

    global open_num

    """
    使用TCP握手对给定IP地址上的端口执行状态检查
    """
    # 初始化socket在不同的操作系统
    curr_os = platform.system()
    if curr_os == 'Windows':
        '''
        socket.AF_UNIX：只能够用于单一的Unix系统进程间通信
        socket.AF_INET：服务器之间网络通信
        socket.AF_INET6：IPv6
        socket.SOCK_STREAM：流式socket,for TCP
        socket.SOCK_DGRAM：数据报式socket,for UDP
        socket.SOCK_RAW：原始套接字，普通的套接字无法处理ICMP、IGMP等网络报文，而SOCK_RAW可以；
                        其次，SOCK_RAW也可以处理特殊的IPv4报文；
                        此外，利用原始套接字，可以通过IP_HDRINCL套接字选项由用户构造IP头。
        socket.SOCK_SEQPACKET：可靠的连续数据包服务
        创建TCP Socket：s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        创建UDP Socket：s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
       '''
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        '''
        SO_BINDTODEVICE:可以使socket只在某个特殊的网络接口（网卡）有效。也许不能是移动便携设备
        SO_BROADCAST:允许广播地址发送和接收信息包。只对UDP有效。如何发送和接收广播信息包
        SO_DONTROUTE:禁止通过路由器和网关往外发送信息包。这主要是为了安全而用在以太网上UDP通信的一种方法。
                    不管目的地址使用什么IP地址，都可以防止数据离开本地网络
        SO_KEEPALIVE:可以使TCP通信的信息包保持连续性。这些信息包可以在没有信息传输的时候，使通信的双方确定连接是保持的
        SO_OOBINLINE:可以把收到的不正常数据看成是正常的数据，也就是说会通过一个标准的对recv()的调用来接收这些数据
        SO_REUSEADDR:当socket关闭后，本地端用于该socket的端口号立刻就可以被重用。
                    通常来说，只有经过系统定义一段时间后，才能被重用。
       '''
        # 设置socket选项setsockopt(level,optname,value)和得到socket选项getsockopt()
        # level定义了哪个选项将被使用。通常情况下是SOL_SOCKET，意思是正在使用的socket选项。
        # 这里value设置为1，表示将SO_REUSEADDR标记为TRUE，操作系统会在服务器socket被关闭
        # 或服务器进程终止后马上释放该服务器的端口，否则操作系统会保留几分钟该端口。
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 可以通过设置timeout来限制重连时间，如设置sock.settimeout(20) 那么当socket尝试重连到20秒时，就会停止一切操作。
        sock.settimeout(delay_time)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(delay_time)

    try:
        result = sock.connect_ex((ip, int(port_number)))
        lock.acquire()
        # 如果成功返回0
        if result == 0:
            print('[+] %d open' % port_number)
            open_port.append(port_number)
        open_num += 1
        lock.release()
        sock.close()
    except socket.error as e:
        # 如果失败，意味着端口可能关闭
        pass


def main(ip, port_num):
    threads = []
    delay_time = 1
    open_port_list = []
    for p in port_num:
        t = threading.Thread(target=tcp_connect, args=(ip, p, delay_time, open_port_list))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return open_port_list


if __name__ == '__main__':
    print(main('61.135.169.125', [80, 443, 21, 8080, 9090]))
