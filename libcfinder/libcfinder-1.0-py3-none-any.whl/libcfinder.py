import requests
import os
import pkg_resources
from bs4 import BeautifulSoup

def get_symbols_dict(filename):
    f = open(filename, "r")
    symbols = {}
    for line in f.read().split("\n"):
        if line.strip() == "":
            continue
        fun_offset = line.split(" ")
        symbols[fun_offset[0]] = int(fun_offset[1],16)
    f.close()
    return symbols

def get_lib_offset(fun):
    offsets = {}
    for filename in os.listdir(get_file("")):
        symbols = get_symbols_dict(get_file(filename))
        offsets[filename] = symbols[fun]
    return offsets

def get_file(path):
    _ROOT = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(_ROOT, 'db', path)

def update():
    #domain = "https://libc.nullbyte.cat/"
    domain = "https://libc.blukat.me/"

    r = requests.get(domain+"?q=_rtld_global%3A0")
    soup = BeautifulSoup(r.content,'html5lib')

    libs = []
    for lib in soup.find_all("a", {"class": "lib-item"}):
        libs.append(lib.string.strip())

    if not os.path.exists(get_file("")):
        os.makedirs(get_file(""))

    for lib in libs:
        if os.path.exists(get_file(lib+".symbols")):
            continue
        r = requests.get(domain+"/d/"+lib+".symbols")
        f = open(get_file(lib+".symbols"), "w")
        f.write(r.text)
        f.close()

def find_libcv(functions):    
    for i in range(2):
        found_list = []
        funs_libs = {fun:get_lib_offset(fun) for fun in functions}
        libs = set()
        for fun in funs_libs:
            libs.update(funs_libs[fun].keys())
        for lib in libs:
            for fun in functions:
                if functions[fun] % 0x1000 != funs_libs[fun][lib] % 0x1000:
                    break
            else:
                found_list.append(lib[:-len(".symbols")])

        if len(found_list) == 0:
            print("libc version not found, updating...")
            update()
        else:
            return found_list

    return found_list

def find_fun_addr(libcv, kfun_name, kfun_addr, wfun_name):
    symbols = get_symbols_dict(get_file(libcv+".symbols"))
    return kfun_addr-symbols[kfun_name]+symbols[wfun_name]