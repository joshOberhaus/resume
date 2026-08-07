FROM texlive/texlive:latest

ENV DEBIAN_FRONTEND=noninteractive

# Install Node.js LTS (for yamlresume), git, and python3/pip (ruff isn't
# packaged in Debian's apt repos, so it and pre-commit are installed via pip
# instead; yamllint is available via apt)
RUN apt-get update && apt-get install -y curl git python3 python3-pip yamllint && \
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

RUN npm install -g yamlresume@latest
RUN pip install --break-system-packages ruff pre-commit

# The base image already ships a non-root "texlive" user (uid/gid 1000);
# reuse it instead of creating another, so files in the mounted workspace
# aren't owned by root. VS Code remaps this uid/gid to the host user
# automatically (see devcontainer.json's updateRemoteUserUID).
USER texlive
