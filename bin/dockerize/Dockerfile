FROM ubuntu:latest

RUN apt update -y && apt upgrade -y
RUN apt install -y clang python3-full curl zsh python3-pip git
RUN apt install -y lsb-release
RUN <<HERE bash
	python3 -m venv /root/.venv
	source /root/.venv/bin/activate
	python3 -m pip install --upgrade pip setuptools
	python3 -m pip install norminette
	echo "export PATH=\$PATH:/root/.venv/bin" >> /root/.zshrc
	deactivate
	bash -c "\$(curl -fsSL https://raw.github.com/xicodomingues/francinette/master/bin/install.sh)"
HERE

RUN <<__EOF__
	echo >/usr/bin/murminette <<eof \
	\#! /usr/bin/bash \\n \
	zsh -l -c \""cd /tmp/proj && source /root/.zshrc && /root/francinette/tester.sh \$@"\" \
	<<eof
__EOF__

# RUN <<__EOF__ tee /usr/bin/murminette
# #! /usr/bin/bash
# zsh -l -c "cd /tmp/proj && source /root/.zshrc && /root/francinette/tester.sh \$@"
# __EOF__

RUN chmod +x /usr/bin/murminette

# CMD [ "cat", "/usr/bin/murminette" ]
CMD [ "murminette" ]
