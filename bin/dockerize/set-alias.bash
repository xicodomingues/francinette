line="alias murminette='docker run --rm -v .:/tmp/proj \`curl https://raw.githubusercontent.com/murmurlab/francinette/refs/heads/murmurlab-docker/bin/dockerize/Dockerfile | docker build -q -\`'"
>>~/.bash_profile cat <<END
$line
END
>>~/.zshrc cat <<END
$line
END