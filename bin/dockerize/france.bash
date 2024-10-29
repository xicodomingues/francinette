python3 -m venv /root/.venv
source /root/.venv/bin/activate
python3 -m pip install --upgrade pip setuptools
python3 -m pip install norminette
echo "export PATH=\$PATH:/root/.venv/bin" >> /root/.zshrc
bash -c "$(curl -fsSL https://raw.github.com/xicodomingues/francinette/master/bin/install.sh)"
deactivate