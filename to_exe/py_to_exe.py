# Author pengzihao
# Date 2019/1/8
"""
将calculator项目转换为exe文件
"""
from PyInstaller.__main__ import run

if __name__ == '__main__':
    opts = ['screen_recorder_demo.py', '-w', '--onefile']
    # opts = ['douyin.py', '-F']
    # opts = ['douyin.py', '-F', '-w']
    # opts = ['douyin.py', '-F', '-w', '--icon=TargetOpinionMain.ico','--upx-dir','upx391w']
    run(opts)