#!/bin/bash

# Quick and dirty script to allow me to port from ec2s during development.

log() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $1..."
}

# Update system packages
log "Starting system update"
sudo apt-get update -y

# Install required packages
log "Installing required packages"

install_docker() {
    log "Installing Docker"

    # Prepare Docker repository
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # Test Docker installation
    sudo docker run hello-world
    log "Docker installation completed"
}

#create_docker_user() {
#    log "Creating a dedicated Docker user"

    # Create a new user without password, add to docker group
#    sudo useradd -m -s /bin/bash dockeruser
#    sudo usermod -aG docker dockeruser
#    echo "dockeruser ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/dockeruser
#
#    log "Docker user created and added to the Docker group"
#}

install_docker_compose() {
    log "Installing Docker Compose"

    # Install Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    # Verify installation
    docker-compose --version
    log "Docker Compose installation completed"
}

deploy() {
    docker pull daveved/little-daveved-web-app
    docker run -d -p 8001:8001 daveved/little-daveved-web-app
}
# Main execution flow
install_docker
install_docker_compose
deploy

log "Deployment script execution completed"