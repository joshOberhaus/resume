FROM texlive/texlive:latest

ENV DEBIAN_FRONTEND=noninteractive

# Install Node.js LTS (for yamlresume) and git
RUN apt-get update && apt-get install -y curl git && \
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

RUN npm install -g yamlresume@latest
