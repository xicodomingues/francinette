FROM ubuntu:latest

RUN apt update -y && apt upgrade -y
RUN apt install -y clang python3-full curl zsh python3-pip git
RUN apt install -y lsb-release
RUN curl https://raw.githubusercontent.com/murmurlab/francinette/refs/heads/murmurlab-docker/bin/dockerize/france.bash -o /tmp/f.bash
RUN ["/bin/bash", "/tmp/f.bash"]

CMD [ "zsh","-l" ,"-c", "cd /tmp/proj && source /root/.zshrc && /root/francinette/tester.sh" ]
