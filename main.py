"""One-line office joke entry for make.fun.

Writes the entry to /output/entry.txt.
Python 3, standard library only.
"""

import os

JOKE = "My boss said we have unlimited PTO, which explains why nobody here has ever taken a day off."


def main():
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(JOKE)
    print("wrote %d characters to /output/entry.txt" % len(JOKE))


if __name__ == "__main__":
    main()
