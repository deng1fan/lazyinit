import os
from lazyinit.utils import show_available_version, run_cmd, echo, run_cmd_inactivate


def init():
    if "bash" not in run_cmd("echo $SHELL", show_cmd=False):
        if "bash" not in run_cmd("cat /etc/shells", show_cmd=False):
            echo("未找到 bash 环境，请先安装 bash 环境！", "red")
        else:        
            echo("请在 bash 环境下运行本工具！")
        echo("您可以通过以下命令查看所支持的 Shell 类型：\ncat /etc/shells", "red")
        echo("您可以通过以下命令切换 Shell 类型：\nchsh -s /bin/bash", "red")
        exit()

    pkg_current_path = os.path.dirname(os.path.abspath(__file__))
    python_version = "3.9"
    env_name = "lazydl"

    # 读取 ~/.bashrc 文件内容
    if not os.path.exists("~/.bashrc"):
        run_cmd("touch ~/.bashrc", show_cmd=False)
    bashrc = run_cmd("cat ~/.bashrc", show_cmd=False)
    if "lazyinit" not in bashrc:
        print("未找到 lazyinit 配置，即将注入配置到 ~/.bashrc（完成后可能需要重启初始化工具）")
        # ---------------------------------------------------------------------------- #
        #                         配置 Bash 环境变量                                     
        # ---------------------------------------------------------------------------- #
        bash = [
            "cd ~/",
            "cat {}/bash_config.txt >> ~/.bashrc".format(pkg_current_path),
        ]
        run_cmd(bash, show_cmd=False)
        echo("运行 {} 以完成配置（运行后需要重启工具）".format("source ~/.bashrc"), "yellow")
        exit(0)
        
    echo("")
    echo("")
    echo("")
    echo("")
    echo("")
    echo("         __                         __  ___      __                ____")
    echo("        / /   ____ _____  __  __   /  |/  /___ _/ /_____  _____   / __ )__  _________  __")
    echo("       / /   / __ `/_  / / / / /  / /|_/ / __ `/ //_/ _ \\/ ___/  / __  / / / / ___/ / / /")
    echo("      / /___/ /_/ / / /_/ /_/ /  / /  / / /_/ / ,< /  __(__  )  / /_/ / /_/ (__  ) /_/ /")
    echo("     /_____/\\__,_/ /___/\\__, /  /_/  /_/\\__,_/_/|_|\\___/____/  /_____/\\__,_/____/\\__, /")
    echo("                       /____/                                                   /____/")
    echo("")
    echo("")
    echo("")
    echo("")

 
    step = "-1"
    while step != "0":
        if step != "-1":
            echo("\n是否继续配置？（y/n）", "yellow")
            conti = input()
            if conti != "y":
                break
        echo(" ", "blue")
        echo("1、设置 pip 源", "blue") 
        echo("2、安装 MiniConda", "blue")
        echo("3、安装 ranger 并自动配置", "blue")
        echo("4、新建虚拟环境", "blue")
        echo("5、安装 Redis", "blue")
        echo("6、生成公钥", "blue")
        echo("7、生成 lazydl 项目模板", "blue")
        echo("0、退出", "blue")
        echo(" ", "blue")
        echo("请在下方输入操作序号：", "yellow")
        step = input()
        if step == "1":
            # ---------------------------------------------------------------------------- #
            #                         设置 pip 源                                     
            # ---------------------------------------------------------------------------- #
            pip_source = [
                "conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/",
                "conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/",
                "conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/",
                "conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/",
                "conda config --set show_channel_urls yes",
                "pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple",
                "pip config set global.extra-index-url https://pypi.org/simple"
            ]
            run_cmd(pip_source)
        
        elif step == "2":
            # ---------------------------------------------------------------------------- #
            #                         安装 MiniConda                                     
            # ---------------------------------------------------------------------------- #
            run_cmd_inactivate([
                "wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh",
                "sh Miniconda3-latest-Linux-x86_64.sh",
            ])

        elif step == "3":
            # ---------------------------------------------------------------------------- #
            #                             安装 ranger                                 
            # ---------------------------------------------------------------------------- #
            ranger = [
                "python -m pip install ranger-fm",
                "mv {}/ranger ~/.config/".format(pkg_current_path),
            ]
            run_cmd(ranger)

        elif step == "4":
            # ---------------------------------------------------------------------------- #
            #                         创建 lazydl 环境                                     
            # ---------------------------------------------------------------------------- #
            echo("即将创建新环境，请在下方输入 Python 版本号，默认为 3.9：", "yellow")
            python_version = input()
            if python_version == "":
                python_version = "3.9"
            echo("即将创建新环境，请在下方输入环境名称，将会自动安装 lazydl 包，默认名称为 lazydl：", "yellow")
            env_name = input()
            if env_name == "":
                env_name = "lazydl"
            
            run_cmd_inactivate("conda create -n {} python={} pandas".format(env_name, python_version))
            
            echo("访问 Pytorch 官网获取最新安装命令：https://pytorch.org/get-started/locally/")
            echo("请在下方手动切换到 {} 环境并输入 Pytorch 安装命令运行：".format(env_name), "yellow")
            # pytorch_install = input()
            # run_cmd_inactivate(pytorch_install)
        

        elif step == "5":
            echo("安装 Redis 时间可能较长（大约五分钟），请耐心等待！")
            run_cmd([
                "sh {}/redis.sh".format(pkg_current_path),
                "cp {}/redis.conf ~/redis/bin/".format(pkg_current_path),
                "~/redis/bin/redis-server ~/redis/bin/redis.conf",
            ])
            
        elif step == "6":
            run_cmd_inactivate([
                "cd ~/.ssh",
                "ssh-keygen -t rsa",
                "cat id_rsa.pub"
            ])
            
        elif step == "7":
            echo("请在下方输入 “项目路径”， 默认为 “./lazydl” ：", "yellow")
            target_path = input()
            # if target == "":
            #     target = os.getcwd() + " lazydl"
            # if len(target.split(" ")) != 2:
            #     echo("输入有误，请重新输入！")
            #     continue
            
            # target_path = target.split(" ")[0]
            # target_name = target.split(" ")[1]
            if not os.path.exists(target_path):
                os.makedirs(target_path)
                
            run_cmd([
                "cp -r {}/lazydl {}".format(pkg_current_path, target_path),   
                # "cd {}".format(target_path),
                # "mv lazydl {}".format(target_name),     
            ])
            
        elif step == "0":
            exit()

        else:
            continue
        
        
