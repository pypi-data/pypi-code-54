import fire
from tamplar.api import methods


def main():
    fire.Fire({
        'init': methods.init,
        'deps': methods.deps,
    })


if __name__ == '__main__':
    main()
