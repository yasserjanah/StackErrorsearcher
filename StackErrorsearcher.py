#!/usr/bin/env python3

__author__ = "Yasser Janah"

try:
    import requests
    from subprocess import Popen, PIPE
    import os
    import re
    from argparse import ArgumentParser
    from time import sleep
except ImportError as err:
    print(err)


class msg(object):
    WHITE = u"\u001b[38;5;255m"
    BLACK = u"\u001b[38;5;0m"
    RED = u"\u001b[38;5;196m"
    GREEN = u"\u001b[38;5;40m"
    BLUE = u"\u001b[38;5;21m"
    YELLOW = u"\u001b[38;5;220m"
    MAG = u"\u001b[38;5;125m"
    BLINK = "\033[6m"
    UNDERLINE = "\033[4m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    @staticmethod
    def failure(_msg, very=False):
        text = f""
        if very is True:
            text += f"{msg.RED}[+]{msg.WHITE} {_msg} {msg.RED}not found.{msg.WHITE}"
        else:
            text = f"{msg.RED}[+]{msg.WHITE} {_msg}{msg.WHITE}"
        print(text)

    @staticmethod
    def success(_msg, very=False):
        text = f""
        if very is True:
            text += f"{msg.GREEN}[+]{msg.WHITE} {_msg} {msg.GREEN}found.{msg.WHITE}"
        else:
            text = f"{msg.GREEN}[+]{msg.WHITE} {_msg}{msg.WHITE}"
        print(text)

    @staticmethod
    def warning(_msg, very=False):
        text = f""
        if very is True:
            text += f"{msg.YELLOW}[+]{msg.WHITE} {msg.YELLOW}{_msg}{msg.WHITE}"
        else:
            text = f"{msg.YELLOW}[+]{msg.WHITE} {_msg}{msg.WHITE}"
        print(text)

    @staticmethod
    def info(_msg, very=False):
        text = f""
        if very is True:
            text += f"{msg.BLUE}[+]{msg.WHITE} {msg.BLUE}{_msg}{msg.WHITE}"
        else:
            text = f"{msg.BLUE}[+]{msg.WHITE} {_msg}{msg.WHITE}"
        print(text)


def exec_(cmd):
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    if err != b'':
        # found an error
        err_txt = err.decode().split('\n')[-2]
        return err_txt
    else:
        return False


def make_cmd(args):
    cmd = []
    for _a in args:
        cmd.append(_a)
    return cmd


def cal_(x):
    c = 0
    for i in x['items']:
        if i['is_answered']:
            c += 1
    return c


def search_(err_txt):
    req = requests.get(
        'https://api.stackexchange.com/2.2/search?order=desc&sort=activity&tagged=python&intitle={0}&site=stackoverflow'.format(err_txt))
    all_errors = req.json()['items']
    msg.success("found {0}{1}{2} result(s).".format(
        msg.GREEN, len(all_errors), msg.WHITE))
    if len(all_errors) != cal_(req.json()):
        un = len(all_errors) - cal_(req.json())
        msg.warning(
            '{0}{1}{2} Unanswered questions were found, and we will only display the {3}{4}{2} questions that were answered ...'.format(msg.RED, un, msg.WHITE, msg.GREEN, cal_(req.json())))
    for _ in all_errors:
        if _['is_answered']:
            print("")
            print(msg.GREEN+"[+] "+msg.WHITE+msg.BOLD+"title"+msg.RESET+" : "+msg.RESET +
                  msg.YELLOW+"'"+msg.WHITE+_['title'].replace('&quot;', '"')+msg.YELLOW+"'"+msg.WHITE)
            print(msg.GREEN+"[+] "+msg.WHITE+msg.BOLD+"link"+msg.RESET+" : " +
                  msg.RESET+msg.YELLOW+"'"+msg.WHITE+_['link']+msg.YELLOW+"'"+msg.WHITE)
            sleep(0.32)
            #print(msg.GREEN+"\t[+] "+msg.WHITE+msg.BOLD+msg.UNDERLINE+"VIEWS"+msg.RESET+" : "+msg.RESET+str(_['view_count']))
            #print(msg.GREEN+"\t[+] "+msg.WHITE+msg.BOLD+msg.UNDERLINE+"ANSWER"+msg.RESET+" "+msg.UNDERLINE+"COUNT"+msg.RESET+" : "+msg.RESET+str(_['answer_count']))
            #print(msg.GREEN+"\t[+] "+msg.WHITE+msg.BOLD+msg.UNDERLINE+"SCORE"+msg.RESET+" : "+msg.RESET+str(_['score']))
            #print(msg.GREEN+"\t[+] "+msg.WHITE+msg.BOLD+msg.UNDERLINE+"TAGS"+msg.RESET+" : "+msg.RESET+', '.join(_['tags']))


def main():
    parser = ArgumentParser()
    parser.add_argument('--cmd', help='command to run , the program will found automatically the error')
    parser.add_argument('--error-text', help='specify an error message')
    args = parser.parse_args()
    if args.cmd and not args.error_text:
        cmd = make_cmd(args.cmd.split())
        msg.info("executing command "+msg.YELLOW+"'"+msg.WHITE +
                 ' '.join(cmd)+msg.YELLOW+"'"+msg.WHITE+"...")
        err_x = exec_(cmd)
        msg.success("found "+msg.WHITE+"'"+msg.YELLOW +
                    err_x+msg.WHITE+"' "+msg.WHITE+"...")
        sleep(1)
        msg.info("searching for solutions in stackoverflow ...")
        sleep(2)
        search_(err_x)
    elif args.error_text and not args.cmd:
        msg.info("error "+msg.WHITE+"'"+msg.YELLOW +
                 args.error_text+msg.WHITE+"' "+msg.WHITE+"...")
        sleep(1)
        msg.info("searching for solutions in stackoverflow ...")
        sleep(2)
        search_(args.error_text)
    elif args.cmd and args.error_text:
        print("\n --cmd with --error-text not allowed.")
    else:
        parser.print_help()
    print("")


main()
