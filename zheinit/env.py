import os
from zheinit.utils import show_available_version, run_cmd, echo, get_cmd_output
def init():
    if "bash" not in get_cmd_output("echo $SHELL"):
        if "bash" not in get_cmd_output("cat /etc/shells"):
            print("未找到 bash 环境，请先安装 bash 环境！")
        else:        
            print("请在 bash 环境下运行本工具！")
        print("您可以通过以下命令查看所支持的 Shell 类型：\ncat /etc/shells")
        print("您可以通过以下命令切换 Shell 类型：\nchsh -s /bin/bash")
        exit()

    pkg_current_path = os.path.dirname(os.path.abspath(__file__))
    python_version = "3.9"
    env_name = "zhei"

    # 读取 ~/.bashrc 文件内容
    if not os.path.exists("~/.bashrc"):
        run_cmd("touch ~/.bashrc")
    bashrc = get_cmd_output("cat ~/.bashrc")
    if "zhei-init" not in bashrc:
        print("未找到 zhei-init 配置，即将注入配置到 ~/.bashrc（完成后可能需要重启初始化工具）")
        # ---------------------------------------------------------------------------- #
        #                         配置 Bash 环境变量                                     
        # ---------------------------------------------------------------------------- #
        bash = [
            "cd ~/",
            "cat {}/bash_config.txt >> ~/.bashrc".format(pkg_current_path),
            "conda init bash",
            "source ~/.bashrc",
        ]
        run_cmd(bash)
        


    echo("             欢迎使用服务器环境初始化工具 zhei-init ！", "green")
    echo("   本工具将会帮助您初始化服务器环境，下面是功能菜单，可输入序号进行配置", "green")

    step = "-1"
    while step != "0":
        if step != "-1":
            echo("是否继续配置？（y/n）", "yellow")
            conti = input()
            if conti != "y":
                break
        echo(" ", "blue")
        echo("1、设置 pip 源", "blue") 
        echo("2、安装 MiniConda", "blue")
        echo("3、安装 ranger 并自动配置", "blue")
        echo("4、创建 Conda  Pytorch 环境", "blue")
        echo("5、生成公钥", "blue")
        echo("0、退出", "blue")
        echo(" ", "blue")
        echo("请输入操作序号：", "yellow")
        step = input()
        if step == "1":
            # ---------------------------------------------------------------------------- #
            #                         设置 pip 源                                     
            # ---------------------------------------------------------------------------- #
            pip_source = [
                "conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/",
                "conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/",
                "conda config --set show_channel_urls yes",
                "pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple",
                "pip config set global.extra-index-url https://pypi.org/simple"
            ]
            run_cmd(pip_source)
        
        elif step == "2":
            # ---------------------------------------------------------------------------- #
            #                         安装 MiniConda                                     
            # ---------------------------------------------------------------------------- #
            run_cmd([
                "wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh",
                "sh Miniconda3-latest-Linux-x86_64.sh",
            ])

        elif step == "3":
            # ---------------------------------------------------------------------------- #
            #                             安装 ranger                                 
            # ---------------------------------------------------------------------------- #
            ranger = [
                "pip install ranger-fm",
                "mv {}/ranger ~/.config/".format(pkg_current_path),
            ]
            run_cmd(ranger)

        elif step == "4":
            # ---------------------------------------------------------------------------- #
            #                         创建 zhei 环境                                     
            # ---------------------------------------------------------------------------- #
            python_version = input("请输入 Python 版本号，默认为 3.9：")
            env_name = input("请输入环境名称，将会自动安装 zhei 包，默认名称为 zhei：")
            zhei = [
                "conda create -n {} python={}".format(env_name, python_version),
                "conda activate {}".format(env_name),
                "pip install zhei --upgrade",
            ]
            run_cmd(zhei)

            cuda_version = input("请输入 CUDA 版本号：")
            torch_url, torchvision_url, torchaudio_url = show_available_version(cuda_version, python_version)

            print("即将从以下链接安装 torch：\n {}".format(torch_url))
            torch_install = [
                "pip install {}".format(torch_url),
            ]   
            run_cmd(torch_install)

            print("即将从以下链接安装 torchvision：\n {}".format(torchvision_url))  
            torchvision_install = [
                "pip install {}".format(torchvision_url),
            ]
            run_cmd(torchvision_install)

            print("即将从以下链接安装 torchaudio：\n {}".format(torchaudio_url))
            torchaudio_install = [
                "pip install {}".format(torchaudio_url),
            ]   
            run_cmd(torchaudio_install)
            
        elif step == "5":
            run_cmd([
                "cd ~/.ssh",
                "ssh-keygen -t rsa",
                "cat id_rsa.pub"
            ])
            
        elif step == "0":
            exit()

        else:
            continue