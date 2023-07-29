from bs4 import BeautifulSoup
import requests as rq
import pkg_resources
import os
from rich.console import Console
import subprocess
from rich.progress import track

console = Console()

def package_installed(package_name):
    """
    检查指定包是否已安装
    """
    try:
        pkg_resources.get_distribution(package_name)
    except pkg_resources.DistributionNotFound:
        return False
    else:
        return True

def echo(msg, color="green"):
    console.print(msg, style=color)
    

def run_cmd_inactivate(cmd_list):
    if isinstance(cmd_list, str):
        cmd = cmd_list
        print("\n" + cmd)
        while True:
            exitcode = os.system(cmd)
            if exitcode != 0:
                echo("执行 {} 失败！".format(cmd), "#FF6AB3")
                echo("可通过在下方修改命令继续执行，或者直接按下回车键结束操作：")
                cmd = input()
                if cmd == "":   
                    return exitcode
            else:
                return exitcode
            
    outputs = []
    for cmd in track(cmd_list, description="命令执行中", transient=True):
        print("\n" + cmd)
        while True:
            exitcode = os.system(cmd)
            if exitcode != 0:
                echo("执行 {} 失败！".format(cmd), "#FF6AB3")
                echo("可通过在下方修改命令继续执行，或者直接按下回车键结束操作：")
                cmd = input()
                if cmd == "":
                    break
            else:
                break

    return outputs   


def run_cmd(cmd_list, show_cmd=True):
    if isinstance(cmd_list, str):
        cmd = cmd_list
        if show_cmd:
            print("\n" + cmd)
        while True:
            exitcode, output = subprocess.getstatusoutput(cmd)
            if exitcode != 0:
                echo("执行 {} 失败！".format(cmd), "#FF6AB3")
                echo("错误信息：\n{}".format(output))
                echo("可通过在下方修改命令继续执行，或者直接按下回车键结束操作：")
                cmd = input()
                if cmd == "":
                    return output
            else:
                return output
            
    outputs = []
    for cmd in track(cmd_list, description="命令执行中", transient=True):
        if show_cmd:
            print("\n" + cmd)
        while True:
            exitcode, output = subprocess.getstatusoutput(cmd)
            if exitcode != 0:
                echo("执行 {} 失败！".format(cmd), "#FF6AB3")
                echo("错误信息：\n{}".format(output))
                echo("可通过在下方修改命令继续执行，或者直接按下回车键结束操作：")
                cmd = input()
                if cmd == "":
                    outputs.append(output)
                    break
            else:
                outputs.append(output)
                break

    return outputs
        


def show_available_version(cuda_version="11.8", python_version="3.9"):
    url = "https://download.pytorch.org/whl/torch_stable.html"
    html = rq.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    available_items = []
    backup_items = []
    for i, item in enumerate(soup.find_all("a")):
        if "-linux_x86_64.whl" in item.attrs["href"] and "cpu" not in item.attrs["href"]:
            if "/torch-" in item.attrs["href"] or "/torchvision-" in item.attrs["href"] or "/torchaudio-" in item.attrs["href"]:
                if item.attrs["href"].startswith("cu"):
                    backup_items.append(item)
                    if "-cp{}-".format(python_version.replace(".", "")) in item.attrs["href"]:
                        if "cu{}".format(cuda_version.replace(".", "")) in item.attrs["href"] and "-cp{}-".format(python_version.replace(".", "")) in item.attrs["href"]:
                            available_items.append(item)
        
    if len(available_items) == 0:
        print("未找到可用的版本！")
        print("可选的 CUDA 版本号：\n", set([item.attrs["href"].split("/")[0].replace("cu", "") for item in backup_items]))
        print("可选的 Python 版本号：\n", set([item.attrs["href"].split("-")[2].replace("cp", "") for item in backup_items]))
        cuda_version = input("请重新输入兼容的 CUDA 版本号：")
        python_version = input("请重新输入兼容的 Python 版本号：")
        return show_available_version(cuda_version, python_version)
    
    torch_version = []
    torchvision_version = []
    torchaudio_version = []
    for item in available_items:
        if "torch-" in item.attrs["href"]:
            torch_version.append(item.attrs["href"].split("-")[1].split("%")[0])
        if "torchvision-" in item.attrs["href"]:
            torchvision_version.append(item.attrs["href"].split("-")[1].split("%")[0])
        if "torchaudio-" in item.attrs["href"]:
            torchaudio_version.append(item.attrs["href"].split("-")[1].split("%")[0])
    
    echo("可选的 torch 版本号：")
    for i, item in enumerate(set(torch_version)):
        print("{}、 {}".format(i + 1, item))
    selected_torch_version = input("请选择 torch 版本号，输入序号即可：")
    selected_torch_version = list(set(torch_version))[int(selected_torch_version) - 1]
    print("可选的 torchvision 版本号：")
    for i, item in enumerate(set(torchvision_version)):
        print("{}、 {}".format(i + 1, item))
    selected_torchvision_version = input("请选择 torchvision 版本号，输入序号即可：")
    selected_torchvision_version = list(set(torchvision_version))[int(selected_torchvision_version) - 1]
    print("可选的 torchaudio 版本号：")
    for i, item in enumerate(set(torchaudio_version)):
        print("{}、 {}".format(i + 1, item))
    selected_torchaudio_version = input("请选择 torchaudio 版本号，输入序号即可：")
    selected_torchaudio_version = list(set(torchaudio_version))[int(selected_torchaudio_version) - 1]
    
    torch_url = ""
    torchvision_url = ""
    torchaudio_url = ""
    for i, item in enumerate(available_items):
        if "/torch-{}".format(selected_torch_version) in item.attrs["href"]:
            torch_url = "https://download.pytorch.org/whl/" + item.attrs["href"]
        if "/torchvision-{}".format(selected_torchvision_version) in item.attrs["href"]:
            torchvision_url = "https://download.pytorch.org/whl/" + item.attrs["href"]
        if "/torchaudio-{}".format(selected_torchaudio_version) in item.attrs["href"]:
            torchaudio_url = "https://download.pytorch.org/whl/" + item.attrs["href"]
    
    return torch_url, torchvision_url, torchaudio_url
