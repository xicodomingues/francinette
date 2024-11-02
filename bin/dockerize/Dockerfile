FROM ubuntu:latest

RUN apt update -y && apt upgrade -y
RUN apt install -y clang python3-full curl zsh python3-pip git
RUN apt install -y lsb-release
RUN curl https://raw.githubusercontent.com/murmurlab/francinette/refs/heads/murmurlab-docker/bin/dockerize/france.bash -o /tmp/f.bash
RUN ["/bin/bash", "/tmp/f.bash"]
RUN <<__EOF__
	echo >/usr/bin/murminette <<eof \
	\#! /usr/bin/bash \\n \
	zsh -l -c "cd /tmp/proj && source /root/.zshrc && /root/francinette/tester.sh \$@" \
	<<eof
__EOF__
RUN chmod +x /usr/bin/murminette

# CMD [ "cat", "/usr/bin/murminette" ]
CMD [ "murminette" ]
