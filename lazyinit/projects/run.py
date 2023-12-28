import os
from lazyinit.utils import run_cmd, run_cmd_inactivate, echo
import yaml
import datetime
import time


def read_yaml(path):
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    return data


def run():
    
    project_path = os.getcwd()
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
    echo("                                  欢迎使用 LazyDL 项目启动器！")
    echo("")
    echo("当前工作目录为：{}".format(project_path))
    
    # 获取可选的项目名
    projects = os.listdir(os.path.join(project_path, "configs/experiments"))
    echo("\n可选的项目名：")
    for i, project in enumerate(projects):
        if "." in project:
            continue
        echo("{}、 {}".format(i + 1, project), "#FF6AB3")
    
    echo("\n请在下方输入您的项目名或直接选择序号：")
    project_name = input()
    if project_name.isdigit():
        project_name = projects[int(project_name) - 1]
    
    echo("\n选择启动 {} 项目计划的模式，目前支持 “nohup”、“tmux”、“python”，默认为 “nohup”：".format(project_name))
    start_mode = input()
    conda_env = ""
    if start_mode not in ["nohup", "tmux", "python"] or start_mode == "":
        start_mode = "nohup"
    if start_mode == "tmux":
        echo("\n请在下方输入您的 conda 环境名，默认 lazydl：")
        conda_env = input("")
        if conda_env == "":
            conda_env = "lazydl"
            
    
    
    # ---------------------------------------------------------------------------- #
    #                         获取实验计划                                     
    # ---------------------------------------------------------------------------- #
    exp_plan_path = os.path.join(project_path, "configs/experiments/{}/exp_plan.yaml".format(project_name))
    exp_plan = read_yaml(exp_plan_path)
    
    # ---------------------------------------------------------------------------- #
    #                         获取默认配置                                     
    # ---------------------------------------------------------------------------- #
    defalut_exp_cfg = read_yaml(os.path.join(project_path, "configs/default_config.yaml"))
    defalut_exp_cfg_keys = list(defalut_exp_cfg.keys())
    
    
    exp_num = len(exp_plan['experiments'])
    echo("\n本次计划运行 {} 个实验，启动间隔为两分钟！".format(exp_num), "blue")
    
    # ---------------------------------------------------------------------------- #
    #                         逐个启动实验                                     
    # ---------------------------------------------------------------------------- #
    for i, exp_name in enumerate(exp_plan['experiments'].keys()):
        echo("\n正在启动第 {} 个实验：{}".format(i+1, exp_name), "yellow")
        # ---------------------------------------------------------------------------- #
        #                         获取实验配置                                     
        # ---------------------------------------------------------------------------- #
        exp_cfg_path = exp_plan['experiments'][exp_name]['config_path']
        hyper_params = exp_plan['experiments'][exp_name]['hyper_params']
        exp_cfg = read_yaml(os.path.join(project_path, "configs/experiments/{}.yaml".format(exp_cfg_path)))
        exp_cfg_keys = list(exp_cfg.keys())
        all_existed_keys = list(set(defalut_exp_cfg_keys + exp_cfg_keys))
        
        # ---------------------------------------------------------------------------- #
        #                         组装命令行参数                                     
        # ---------------------------------------------------------------------------- #
        hyper_params_str = ""
        if "visible_cuda" in hyper_params:
            visible_cuda = hyper_params["visible_cuda"]
        elif "visible_cuda" in exp_cfg_keys:
            visible_cuda = exp_cfg["visible_cuda"]
        else:
            visible_cuda = defalut_exp_cfg["visible_cuda"]
            
        for hyper_param in hyper_params:
            if hyper_param != "lr":
                hyper_params_value = "\"{}\"".format(hyper_params[hyper_param]) if isinstance(hyper_params[hyper_param], str) else hyper_params[hyper_param]
            else:
                hyper_params_value = hyper_params[hyper_param]
            
            if hyper_param not in all_existed_keys:
                hyper_params_str += " '+{}={}'".format(hyper_param, hyper_params_value)
            else:
                hyper_params_str += " '{}={}'".format(hyper_param, hyper_params_value)
        
    
        if start_mode == "nohup":
            log_path = os.path.join(project_path, "nohup_logs/{}/{}.log".format(project_name, "{}_{}".format(exp_name, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))))
            
            parent_path = "/".join(log_path.split("/")[:-1])
            if not os.path.exists(parent_path):
                os.makedirs(parent_path)
            
            cmd = f"CUDA_VISIBLE_DEVICES={visible_cuda} nohup python run.py"
            cmd += hyper_params_str
            cmd += " +experiments={}".format(exp_cfg_path)
            cmd += " > {} 2>&1 &".format(log_path)
            echo(cmd, "yellow")
            echo("查看日志：tail -f {}".format(log_path))
            run_cmd(cmd, show_cmd=False)
            
        elif start_mode == "python":
            cmd = f"CUDA_VISIBLE_DEVICES={visible_cuda} python run.py"
            cmd += hyper_params_str
            cmd += " +experiments={}".format(exp_cfg_path)
            echo(cmd, "yellow")
            run_cmd_inactivate(cmd)
            
        elif start_mode == "tmux":
            tmux_session = "{}@{}".format(exp_name, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            
            cmd = f"CUDA_VISIBLE_DEVICES={visible_cuda} python run.py"
            cmd += hyper_params_str
            cmd += " +tmux_session=\"{}\"".format(tmux_session)
            cmd += " +experiments={}".format(exp_cfg_path)
            
            run_cmd("tmux new-session -d -s {}".format(tmux_session), show_cmd=False)
            run_cmd("tmux send-keys -t {} cd Space {}".format(tmux_session, project_path), show_cmd=False)
            run_cmd("tmux send-keys -t {} {}".format(tmux_session, "C-m"), show_cmd=False)
            run_cmd("tmux send-keys -t {} conda Space activate Space {}".format(tmux_session, conda_env), show_cmd=False)
            run_cmd("tmux send-keys -t {} {}".format(tmux_session, "C-m"), show_cmd=False)
            run_cmd("tmux send-keys -t {} \"{}\"".format(tmux_session, cmd), show_cmd=False)
            run_cmd("tmux send-keys -t {} {}".format(tmux_session, "C-m"), show_cmd=False)
        
            echo(cmd, "yellow")
            echo("查看实验窗口：tmux attach -t {}".format(tmux_session))
            echo("停止实验：tmux kill-session -t {}".format(tmux_session))
            
        echo("\n实验 {} 已启动！".format(exp_name), "#F48671")
        if i + 1 != exp_num:
            time.sleep(60 * 2)

    
    echo("\n所有实验均已启动！不如趁现在去喝杯咖啡！", "green")
    
# run()
