import json
import os
import socket
import ssl
from urllib.parse import quote
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import validators

FLAGS = ["-h", "-u", "-s"]


class Colors:
    UNDERLINE = '\033[4m'
    FAIL = '\033[91m'
    ENDCOLOR = '\033[0m'
    Red = '\033[31m'
    Green = '\033[32m'
    Blue = '\033[34m'
    Cyan = '\033[36m'


def colored_banner(text, color, end="\n"):
    print(color + text + Colors.ENDCOLOR, end=end)


def help():
    colored_banner("Commands:\n\
            go2web -h               # show help\n\
            go2web -u <URL>         # make an HTTP request to URL and print the response\n\
            go2web -s <search-term> # search the term and print top 10 results", Colors.Blue)


def get_url(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path or "/"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        sslClient = ssl.create_default_context().wrap_socket(client, server_hostname=host)

        sslClient.connect((host, 443))

        request = f"GET {path} HTTP/1.1\r\naccept: text/html\r\nConnection: close\r\nHost: {host}\r\n\r\n"
        sslClient.send(request.encode())

        response = b""
        while True:
            data = sslClient.recv(1024)
            response += data
            if not data or response.endswith(b'\r\n0\r\n\r\n'):
                break

        soup = BeautifulSoup(
            response[response.lower().find(b"<html"):], 'html.parser')
        print(os.linesep.join([s for s in soup.get_text().splitlines() if s]))


def search(search_term):
    search_term_str = ' '.join(search_term)
    encoded_search_term = quote(search_term_str.encode('utf-8'))
    request_url = f"/customsearch/v1?key=AIzaSyD1TY-uJDXAl4m01lCC-orZUfga_D2e_zw&cx=f2ff5f215d5484786&q={encoded_search_term}&start=1&num=10"
    request = f"GET {request_url} HTTP/1.1\r\nConnection: close\r\nHost: www.googleapis.com\r\n\r\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        sslClient = ssl.create_default_context().wrap_socket(
            client, server_hostname="www.googleapis.com")
        sslClient.connect(("www.googleapis.com", 443))
        sslClient.send(request.encode())

        chunks = []
        while True:
            data = sslClient.recv(2048)
            if not data:
                break
            chunks.append(data.decode())

        stringResult = ''.join(chunks)

        response = stringResult[stringResult.find("{"):].replace(
            "\n", "").replace("\r", "")[:-1]

        jsonResult = json.loads(response)

        for index, item in enumerate(jsonResult["items"]):
            print(str(index + 1), end=". ")
            print(item["title"], Colors.UNDERLINE)

        while True:
            colored_banner(
                "To open a link enter any number in range 1-10, 'e' to exit ", Colors.Green)
            colored_banner("--- ", Colors.Red, "")
            input_command = input()

            if(input_command == 'e'):
                break

            try:
                urlNumber = int(input_command)
                if urlNumber > 0 and urlNumber <= 10:
                    get_url(jsonResult["items"][urlNumber - 1]["link"])
                else:
                    print("Wrong command", Colors.FAIL)
            except ValueError:
                print("Wrong command", Colors.FAIL)


def main():
    while True:
        colored_banner(">>> ", Colors.Cyan, "")
        input_command = input()
        command = input_command.split()

        if not validate_command(command):
            continue

        if command[1] == "-h":
            if len(command) > 2:
                colored_banner(
                    "Wrong Command \nType 'go2web -h' for more information", Colors.FAIL)
                continue
            help()
            continue

        if command[1] == "-u":
            if len(command) != 3:
                colored_banner(
                    "The command you entered is not complete, Type 'go2web -h' command for more information", Colors.FAIL)
                continue
            url = command[2]
            if not is_valid_url(url):
                continue
            get_url(url)
            continue

        if command[1] == "-s":
            if len(command) < 3:
                colored_banner(
                    "Wrong command \nSearch command contains <search_tearm>", Colors.FAIL)
                continue
            search_term = command[2:]
            search(search_term)
            continue


def is_valid_url(url):
    is_url_valid = validators.url(url) or validators.domain(url)
    if not is_url_valid:
        colored_banner(
            "Wrong URL, please check the URL and try again", Colors.FAIL)
        return False
    return True


def validate_command(command):
    if len(command) < 2:
        colored_banner(
            "Unknown command, consult -h flag to see available commands", Colors.FAIL)
        return False
    if command[0] != "go2web":
        colored_banner(
            "Your commands must start with: 'go2web' \nCheck -h flag for more information", Colors.FAIL)
        return False
    if command[1] not in FLAGS:
        colored_banner(
            f"Unknown flag \nType the 'go2web -h' to see all commands", Colors.FAIL)
        return False
    return True


main()