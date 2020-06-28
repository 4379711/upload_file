# -*- coding: utf-8 -*-
from PyInstaller.__main__ import run

if __name__ == '__main__':
    # opts = ['client.py', '-w']
    opts = ['server.py', '-F', '-w']
    run(opts)
