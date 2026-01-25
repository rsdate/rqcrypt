import datetime
import time

import colorama

from scrngV2 import random_nums


def example_scrngV2():
    x = datetime.datetime.now()
    start = time.time()
    nums = random_nums(n=10, debug=False)
    end = time.time()
    print(colorama.Style.BRIGHT + "=========== Results ===========")
    print(
        colorama.Fore.BLUE + "Generated numbers:",
        colorama.Style.DIM + str(nums),
    )
    print(
        colorama.Fore.CYAN + "Generation time:",
        colorama.Style.DIM + f"{(end - start):.2f}s",
    )
    print(
        colorama.Fore.RED + "Generation timestamp:",
        colorama.Style.DIM + f"{x.strftime('Generation on %Y-%m-%d at %I:%M.%S %p')}",
    )
