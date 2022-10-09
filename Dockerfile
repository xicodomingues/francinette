FROM ubuntu:22.04

RUN apt-get update && apt-get install -y 
RUN apt-get install clang libpq-dev libbsd-dev libncurses-dev valgrind python3 python3-pip python3-venv python3-wheel -y
RUN apt-get install git -y
RUN pip3 install wheel
RUN pip3 install norminette
RUN apt-get install vim -y

COPY . /root/francinette
RUN rm -rf /root/francinette/venv

WORKDIR /root/francinette

RUN pip3 install -r requirements.txt

WORKDIR /root/project

RUN printf "\nalias paco=%s/francinette/bin/docker_exec.sh\nalias francinette=%s/francinette/bin/docker_exec.sh\n" "$HOME" >> "$HOME/.bashrc"

ENTRYPOINT ["/root/francinette/bin/docker_exec.sh"]

## TODO: write automatic updater for docker version - rebuild when new version is downloaded
## to exec: docker run -it -v $(pwd):/root/project paco
## docker run -it --entrypoint '/bin/bash' -v $(pwd):/root/libft paco