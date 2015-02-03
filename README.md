# Mac DNS Switch
Mac 切换 DNS

### 使用

* 打印帮助信息

		python dns_switch.py -h

* 列出当前设置的 DNS

		python dns_switch.py -c

* 列出当前所有设备

		python dns_switch.py -L
		
* 列出所有可选的 DNS server

		python dns_switch.py -l
	
* 切换 DNS

		python dns_switch.py -d "some device" -s "可选的DNS server"