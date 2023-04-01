import requests
import bs4
import sys

print(sys.argv)

if len(sys.argv) != 3:
    print("Zadej tri argumenty")