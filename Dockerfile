FROM ubuntu:latest

RUN apt update -y && apt upgrade -y
RUN apt install -y clang python3-full curl zsh python3-pip git
RUN apt install -y lsb-release
COPY ./france.bash /tmp/norm.bash

RUN ["/bin/bash", "/tmp/norm.bash"]

CMD [ "zsh","-l" ,"-c", "cd /tmp/proj && ls -la && source /root/.zshrc && /root/francinette/tester.sh" ]