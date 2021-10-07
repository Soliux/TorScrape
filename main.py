import requests, re, socket, threading, queue

moobot = True

class Nodes:
    def __init__(self) -> None:
        self.url = "https://www.dan.me.uk/tornodes"
        open("working.txt", "w").close()

    def _scrape(self) -> None:
        res = requests.get(self.url, proxies=self.proxy)
        if res.status_code == 200:
            print(res.text)


    def _parse(self, file: str) -> list[str]:
        nodelist = []
        ipv6 = re.compile("(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))")
        FILE = open(file, "r", encoding="utf-8").readlines()
        for item in FILE:
            node = item.rstrip("\n")
            ip = node.split("|")[0]
            port = node.split("|")[2]
            if bool(ipv6.match(ip)) == True:
                pass
            else:
                nodelist.append(f"{ip}:{port}")
        print(f"Parsed: {len(nodelist)} Nodes")
        return nodelist

    def _checknode(self, node: str, q: queue.Queue) -> bool:
        ip = node.split(":")[0]
        port = node.split(":")[1]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        try:
            sock.connect((ip, int(port)))
            print(f"Connected to {node}")
            sock.close()
            q.put(True)
            return True
        except:
            print(f"Dead {node}")
            q.put(False)
            return False

    def _writer(self, nodes: list[str]) -> None:
        FILE = open("working.txt", "a")
        if moobot == True:
            for index, node in enumerate(nodes):
                ip = node.split(":")[0].replace(".", ",")
                port = node.split(":")[1]
                func = f"tor_add_sock({index}, INET_ADDR({ip}), HTONS({port}));"
                FILE.write(f"{func}\n")
        else:
            for node in nodes:
                FILE.write(f"{node}\n")


    def _runner(self):
        working = []
        nodelist = self._parse("./nodes.txt")
        my_queue = queue.Queue()
        print("Checking for valid nodes")
        for node in nodelist:
            thread = threading.Thread(target=self._checknode, args=(node, my_queue))
            thread.start()
            if my_queue.get() == True:
                working.append(node)
            else:
                pass
        thread.join()
        print("Writing to file")
        self._writer(working)


Nodes()._runner()