#!/usr/bin/python
# coding: utf-8

import sys
import os
import subprocess
import platform
import re
from optparse import OptionParser
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("switch_dns")

dns_servers = {
	"google" : [
		'8.8.8.8',
		'8.8.4.4'
	],

	"opendns" : [
		'208.67.222.222',
		'208.67.220.220'
	],

	"opendns family" : [
		'208.67.222.123',
		'208.67.220.123'
	],

	"v2ex" : [
		'199.91.73.222',
		'178.79.131.110'
	],

	"dyn dns" : [
		'216.146.35.35',
		'216.146.36.36'
	],

	"comodo secure" : [
		'8.26.56.26',
		'8.20.247.20'
	],

	"ultradns" : [
		'156.154.70.1',
		'156.154.71.1'
	],

	"Norton ConnectSafe" : [
		'199.85.126.10',
		'199.85.127.10'
	],

	"taiwan zhonghua dianxin" : [
		'168.95.1.1',
		'168.95.192.1',
		'168.95.192.2'
	],

	"114" : [
		'114.114.114.114',
		'114.114.115.115'
	]
}

dns_servers_url = {
	"google" : "",
	"opendns" : "",
	"v2ex" : "http://dns.v2ex.com/",
	"114dns" : ""
}

def cmd_networksetup(sub_cmd):
	cmd = ['networksetup']
	cmd += sub_cmd
	pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return pipe.communicate()

def list_devices():
	cmd = ["-listnetworkserviceorder"]
	output = cmd_networksetup(cmd)
	if output[1]:
		print output[1]
		sys.exit(-1)
	print output[0]

def list_dns_servers():
	for k,v in dns_servers.items():
		print "%s :" %k
		for server in v:
			print " "*4 + server

def switch_dns(device, server):
	sub_cmd = ["-setdnsservers", device] + dns_servers[server]
	output = cmd_networksetup(sub_cmd)
	if output[1]:
		print output[1]
		sys.exit(-1)
	print "设置完成"
	if output[0]:
		print output[0]

def show_dns():
	devices = get_devices()
	for device in devices:
		sub_cmd = ["-getdnsservers", device]
		output = cmd_networksetup(sub_cmd)
		if output[1]:
			print output[1]
			sys.exit(-1)
		print device + " :"
		for i in output[0].split("\n"):
			print " "*4 + i

def get_devices():
	cmd = ["-listnetworkserviceorder"]
	output = cmd_networksetup(cmd)
	if output[1]:
		print output[1]
		sys.exit(-1)
	device_pattern = "\(\d+\)\s*([^\n]+?)\n"
	match = re.findall(device_pattern, output[0])
	return match

parser = OptionParser()
add_option = parser.add_option
add_option("-L", action="store_true", dest="list_devices", help=u"列出所有网络设备")
add_option("-l", action="store_true", dest="list_dns_servers", help=u"列出所有可选的dns server")
add_option("-c", action="store_true", dest="show_dns", help=u"列出当前的dns")
add_option("-d", dest="device", help=u"需要设置的网络设备")
add_option("-s", dest="server", help=u"设置为哪一个dns server")

def main():
	(options,args) = parser.parse_args()
	if options.list_dns_servers:
		list_dns_servers()
	elif options.list_devices:
		list_devices()
	elif options.show_dns:
		show_dns()
	elif options.device and options.server:
		switch_dns(options.device, options.server)
	else:
		print "-h 打印帮助信息"

if __name__ == '__main__':
	main()

