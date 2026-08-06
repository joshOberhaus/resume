FROM texlive/texlive:latest

ENV DEBIAN_FRONTEND=noninteractive

# Install Node.js LTS (for yamlresume), git, and PyYAML (for the overlay
# merge scripts in scripts/)
RUN apt-get update && apt-get install -y curl git python3-yaml && \
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

RUN npm install -g yamlresume@latest

# Non-root user matching the host user, so files created in the mounted
# workspace aren't owned by root. VS Code remaps this UID/GID to the host
# user automatically (see devcontainer.json's updateRemoteUserUID).
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
# texlive/texlive:latest already ships a group/user with GID/UID 1000, so
# rename it to vscode instead of creating a new one.
RUN groupmod -n $USERNAME $(getent group $USER_GID | cut -d: -f1) \
    && usermod -l $USERNAME -g $USER_GID -d /home/$USERNAME -m -s /bin/bash $(getent passwd $USER_UID | cut -d: -f1)

USER $USERNAME
