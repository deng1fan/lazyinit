conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple



apt-get update && apt-get install -y tmux
pip install ranger-fm


cd ~/.config
git clone https://github.com/appleloveme/ranger

cd ..
git clone https://github.com/appleloveme/Init-Pytorch-Environment.git
cat Init-Pytorch-Environment/bash_config.txt >> ~/.bashrc
source ~/.bashrc

conda create -n zhei python=3.8
conda init bash && source /root/.bashrc
conda activate zhei
pip install zhei --upgrade




cd ~/.ssh
ssh-keygen -t rsa
cat id_rsa.pub