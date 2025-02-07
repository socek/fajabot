from icecream import ic
from icecream import install

from fajabot.application import Application
from fajabot.application import main

if __name__ == "__main__":
    install()
    ic.configureOutput(includeContext=True)

    main()
