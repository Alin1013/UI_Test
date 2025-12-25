# -*- coding:utf-8 -*-

#主代码运行文件

import os
import sys
import time
import subprocess
from pathlib import Path

from pandas.io.formats.format import buffer_put_lines

from Config.Config import Config

def run_command(command,description,log_file=None):
    # 运行命令并实时显示输出，同时保存到日志文件
    print(f"\n{'='*60}")
    print(f"正在执行: {description}")
    print(f"命令: {command}")
    print(f"\n{'='*60}")

    #日志文件
    log_content=[]
    if log_file:
        log_content.append(f"\n{'='*60}")
        log_content.append(f"执行时间：{time.strftime('%Y-%m-%d %H:%M:%S')}")
        log_content.append(f"正在执行:{description}")
        log_content.append(f"命令:{command}")
        log_content.append(f"\n{'='*60}")

    try:
        #终端展示实时输出
        process=subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        for line in iter(process.stdout.readline, ''):
            if line:
                line_content = line.rstrip()
                print(line_content)
                if log_file:
                    log_content.append(line_content)
        process.stdout.close()
        return_code = process.wait()

        #记录执行结果
        if return_code==0:
            result_msg=f"\n ✅{description}执行成功"
            print(result_msg)
            if log_file:
                log_content.append(result_msg)
        else:
            result_msg=f"\n ❌{description}执行失败"
            print(result_msg)
            if log_file:
                log_content.append(result_msg)

        #保存日志到文件
        if log_file and log_content:
            try:
                with open(log_file,"a",encoding="utf-8") as f:
                    f.write("\n".join(log_content)+'\n')
                print(f"日志已经保存到:{log_file}")
            except Exception as e:
                print(f"日志保存失败:{e}")

        return return_code==0
    except Exception as e:
        error_msg=f"\n ❌{description}执行出错:{str(e)}"
        print(error_msg)
        if log_file:
            try:
                with open(log_file,"a",encoding="utf-8") as f:
                    f.write("\n".join(log_content)+'\n' + error_msg+'\n')
            except:
                pass
        return False

def check_directories():
    #检查相关目录是否创建
    directories=[
        Config.test_result_dir,
        Config.test_report_dir,
        Config.test_screenshot_dir,
        "tracing_files"
    ]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"相关目录已确认✅{directory}")
