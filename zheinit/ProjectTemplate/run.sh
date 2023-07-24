ADD_COLOR(){
    RED_COLOR='\E[1;31m'
    GREEN_COLOR='\E[1;32m'
    YELLOW_COLOR='\E[1;33m'
    BLUE_COLOR='\E[1;34m'
    PINK_COLOR='\E[1;35m'
    RES='\E[0m'
    
    #这里判断传入的参数是否不等于2个，如果不等于2个就提示并退出
    if [ $# -ne 2 ];then
        echo "Usage $0 content {red|yellow|blue|green|pink}"
        exit
    fi
    case "$2" in
        red|RED)
            echo -e "${RED_COLOR}$1"
        ;;
        yellow|YELLOW)
            echo -e "${YELLOW_COLOR}$1"
        ;;
        green|GREEN)
            echo -e "${GREEN_COLOR}$1"
        ;;
        blue|BLUE)
            echo -e "${BLUE_COLOR}$1"
        ;;
        pink|PINK)
            echo -e "${PINK_COLOR}$1"
        ;;
        *)
            echo -e "请输入指定的颜色代码：{red|yellow|blue|green|pink}"
    esac
}

SEND_KEYS(){
    tmux send-keys -t "$2"  "$1"
}

# 项目变化时自动变换路径
base_path=$(pwd)
export PYTHONPATH=$base_path
read -p "请输入要运行的实验项目名称：" project_name
exps=(`cat configs/experiments/$project_name/experimental_plan.yaml | shyaml keys experiments`)

exps_num=${#exps[@]}  # 实验数量

run_num=0  # 已经运行的实验数量

ADD_COLOR "\n本次计划实验共有：$exps_num 个\n" yellow

day_time=$(date "+%Y-%m-%d")
hour_time=$(date "+%H-%M-%S")

experiment_plan_id=$day_time-$hour_time

for exp in ${exps[@]};
do
    run_num=$((run_num+1))
    ADD_COLOR "🎬🎬🎬   $run_num、 启动 $exp 实验！  🎬🎬🎬" green

    # 获取配置文件中的参数
    config_name=`cat configs/experiments/$project_name/experimental_plan.yaml | shyaml get-value 'experiments.'$exp'.config_name'`
    exp_keys=`cat configs/experiments/$project_name/experimental_plan.yaml | shyaml keys 'experiments.'$exp`
    config_keys=`cat configs/experiments/$config_name.yaml | shyaml keys`
    default_config_keys=`cat configs/default_config.yaml | shyaml keys`
    sweep_args=""
    if [[ ${exp_keys[@]}  =~ "hyper_params"  ]]; then
        hyper_params=`cat configs/experiments/$project_name/experimental_plan.yaml | shyaml keys 'experiments.'$exp'.hyper_params'`
        for hyper_param_key in ${hyper_params[@]};
        do
            hyper_param_value=`cat configs/experiments/$project_name/experimental_plan.yaml | shyaml get-value 'experiments.'$exp'.hyper_params.'$hyper_param_key`
            SUB="'"
            if [[ $hyper_param_value =~ ^(\.[0-9]+|[0-9]+(\.[0-9]*)?)$ ]]; then
                sub_sweep_args=$hyper_param_key"="$hyper_param_value
            else
                sub_sweep_args=$hyper_param_key"=\\\""$hyper_param_value"\\\""
            fi
            if [[ $config_keys =~ $hyper_param_key ]]; then
                sweep_args=$sweep_args${sub_sweep_args//" "/""}" "
            else
                if [[ $default_config_keys =~ $hyper_param_key ]]; then
                    sweep_args=$sweep_args${sub_sweep_args//" "/""}" "
                else
                    sweep_args=$sweep_args"+"${sub_sweep_args//" "/""}" "
                fi
            fi
        done
    fi

    experiment="+experiments="$config_name
    ADD_COLOR "Using experiment: "$experiment pink

    ADD_COLOR "$exp使用的超参数如下：" pink
    all_args=$sweep_args"fast_run=False use_gpu=True wait_gpus=True force_reload_data=True logger=comet "$experiment
    ADD_COLOR "$all_args" pink

    # 使用 tmux 启动实验
    tmux_session=${exp//" "/"--"}-$day_time-$hour_time
    tmux new-session -d -s $tmux_session
    ADD_COLOR "tmux session name: "${exp//" "/"--"}-$day_time-$hour_time pink
    SEND_KEYS "cd "$base_path $tmux_session
    SEND_KEYS C-m $tmux_session
    SEND_KEYS "conda activate lightning" $tmux_session
    SEND_KEYS C-m $tmux_session
    SEND_KEYS C-m $tmux_session
    run_command="python run.py $sweep_args +tmux_session=$tmux_session +experiment_plan_id=$experiment_plan_id comet_name=$exp fast_run=False use_gpu=True wait_gpus=True force_reload_data=True logger=comet "$experiment

    SEND_KEYS "$run_command" $tmux_session
    SEND_KEYS C-m $tmux_session

    # 防止误占 GPU
    if [ $run_num -lt $exps_num ]; then
        ADD_COLOR "等待 5 秒钟，防止误占 GPU ......" red
        sleep 5
    fi
    ADD_COLOR "" red
done


ADD_COLOR "\n🎉🎉🎉    实验计划已经全部启动！后续请关注 Comet.ml 和 钉钉 获取最新动态！       🎉🎉🎉\n" yellow
ADD_COLOR "📍📍📍  Tips: " blue
ADD_COLOR "👉👉👉  使用 tmux a -t [session_name] 命令查看实验进度！                👈👈👈" blue
ADD_COLOR "👉👉👉  使用 tmux kill-session -t [session_name] 命令结束指定实验！     👈👈👈" blue
ADD_COLOR "👉👉👉  使用 tmux ls 命令查看所有实验！                                 👈👈👈" blue
ADD_COLOR "👉👉👉  使用 tmux kill-session -a 命令结束所有实验！                    👈👈👈" blue
ADD_COLOR "" blue


