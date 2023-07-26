import os
from lazyinit.utils import run_cmd, echo
import yaml
import datetime
import time


def read_yaml(path):
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    return data


def run():
    
    # project_path = "/Users/dengyifan/Desktop/Github仓库/zheinit/zheinit/ProjectTemplate"
    project_path = os.getcwd()
    echo("")
    echo("")
    echo("")
    echo("      _____                          _      ____                  _")
    echo("     |  __ \\                        | |    |  _ \\                | |")
    echo("     | |__) |____      _____ _ __ __| |    | |_) |_   _          | |")
    echo("     |  ___/ _ \\ \\ /\\ / / _ \\ '__/ _` |    |  _ <| | | |     _   | |")
    echo("     | |  | (_) \\ V  V /  __/ | | (_| |    | |_) | |_| |    | |__| |")
    echo("     |_|   \\___/ \\_/\\_/ \\___|_|  \\__,_|    |____/ \\__, |     \\____/")
    echo("                                                   __/ |")
    echo("                                                  |___/")
    echo("")
    echo("")
    echo("")
    echo("                      欢迎使用 zhei 项目启动器！")
    echo("")
    echo("当前工作目录为：{}".format(project_path))
    
    # 获取可选的项目名
    projects = os.listdir(os.path.join(project_path, "configs/exps"))
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
        echo("\n请在下方输入您的 conda 环境名，默认 zhei：")
        conda_env = input("")
        if conda_env == "":
            conda_env = "zhei"
    
    # ---------------------------------------------------------------------------- #
    #                         获取实验计划                                     
    # ---------------------------------------------------------------------------- #
    exp_plan_path = os.path.join(project_path, "configs/exps/{}/exp_plan.yaml".format(project_name))
    exp_plan = read_yaml(exp_plan_path)
    
    # ---------------------------------------------------------------------------- #
    #                         获取默认配置                                     
    # ---------------------------------------------------------------------------- #
    defalut_exp_cfg = read_yaml(os.path.join(project_path, "configs/default_config.yaml"))
    defalut_exp_cfg_keys = list(defalut_exp_cfg.keys())
    
    
    exp_num = len(exp_plan['experiments'])
    echo("\n本次计划运行 {} 个实验".format(exp_num), "blue")
    
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
        exp_cfg = read_yaml(os.path.join(project_path, "configs/exps/{}.yaml".format(exp_cfg_path)))
        exp_cfg_keys = list(exp_cfg.keys())
        all_existed_keys = list(set(defalut_exp_cfg_keys + exp_cfg_keys))
        
        # ---------------------------------------------------------------------------- #
        #                         组装命令行参数                                     
        # ---------------------------------------------------------------------------- #
        hyper_params_str = ""
        for hyper_param in hyper_params:
            hyper_params_value = "\"{}\"".format(hyper_params[hyper_param]) if isinstance(hyper_params[hyper_param], str) else hyper_params[hyper_param]
            
            if hyper_param not in all_existed_keys:
                hyper_params_str += " +{}={}".format(hyper_param, hyper_params_value)
            else:
                hyper_params_str += " {}={}".format(hyper_param, hyper_params_value)
        
    
        if start_mode == "nohup":
            log_path = os.path.join(project_path, "logs/{}/{}.log".format(project_name, "{}_{}".format(exp_name, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))))
            cmd = "nohup python run.py"
            cmd += hyper_params_str
            cmd += " +experiments={}".format(exp_cfg_path)
            cmd += " > {} 2>&1 &".format(log_path)
            echo(cmd, "yellow")
            echo("查看日志：tail -f {}".format(log_path))
            run_cmd(cmd)
            
        elif start_mode == "python":
            cmd = "python run.py"
            cmd += hyper_params_str
            cmd += " +experiments={}".format(exp_cfg_path)
            echo(cmd, "yellow")
            run_cmd(cmd)
            
        elif start_mode == "tmux":
            tmux_session = "{}@{}".format(exp_name, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            
            cmd = "python run.py"
            cmd += hyper_params_str
            cmd += " +tmux_session=\"{}\"".format(tmux_session)
            cmd += " +experiments={}".format(exp_cfg_path)
            
            run_cmd("tmux new-session -d -s {}".format(tmux_session))
            run_cmd("tmux send-keys -t {} {}".format(tmux_session, "cd {}".format(project_path)))
            run_cmd("tmux send-keys -t {} {}".format(tmux_session, "C-m"))
            run_cmd("tmux send-keys -t {} {}".format(tmux_session, "conda activate {}".format(conda_env)))
            run_cmd("tmux send-keys -t {} {}".format(tmux_session, "C-m"))
            run_cmd("tmux send-keys -t {} {}".format(tmux_session, cmd))
            run_cmd("tmux send-keys -t {} {}".format(tmux_session, "C-m"))
        
            echo(cmd, "yellow")
            echo("查看日志：tmux attach -t {}".format(tmux_session))
            echo("关闭日志：tmux kill-session -t {}".format(tmux_session))
            run_cmd(cmd)
            
        echo("实验 {} 已启动！".format(exp_name), "#F48671")
        time.sleep(5)

    
    echo("\n所有实验均已启动！祝好运！", "green")
    
# run()
