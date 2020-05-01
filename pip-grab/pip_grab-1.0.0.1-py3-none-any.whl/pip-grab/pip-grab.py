import subprocess
from datetime import datetime
import time


def grab():
    output = subprocess.check_output("pip freeze")
    output = output.decode("utf-8")
    # print(output)
    lines = output.split("\r\n")
    for line in lines:
        if line.startswith("WARNING"):
            lines.remove(line)

    return lines


def save(packages):
    filename = "data/" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

    with open(filename, "w") as afile:
        for package in packages:
            afile.write(package + "\n")


def install(filename):
    output = subprocess.check_output(f"pip install -r {filename}")
    output = output.decode("utf-8")
    print(output)
    return output


def ticker(duration):
    print("[+] Loop Started")
    print(f"[+] Enivronment grabs after every {duration/60**3} hours")
    while True:
        packages = grab()
        save(packages)
        sleep(duration)


def sleep(n):
    for i in range(n):
        time.sleep(1)


# packages = grab()
# save(packages)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Grabs currently installed pip packages."
    )
    # parser.add_argument('module', metavar='grab', type=str, nargs='+', help='Runs the module')
    # parser.add_argument('module', metavar='module_name', type=str, nargs='+', help='Runs the module')
    parser.add_argument("-s", "--save", action="store_true", help="Save packages")
    parser.add_argument("-g", "--grab", action="store_true", help="Display packages")
    parser.add_argument(
        "-t", "--ticker", type=int, help="Save installed packages after N seconds",
    )

    args = parser.parse_args()

    if args.grab:
        packages = grab()
        for package in packages:
            print(package)

    if args.save:
        packages = grab()
        save(packages)

    if args.ticker:
        ticker(args.ticker)
