#!/bin/bash

# Quick and dirty script enabling clean deployments to ubuntu EC2 instances.
# It ensures all required dependencies are installed, cleans any pre-existing
# deployments, and deploys a clean build.
# Must be run as root ulness you setup the user (commented out here)

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

install_docker_compose() {
    log "Installing Docker Compose"

    # Install Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/download/$(sudo curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d '"' -f 4)/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    # Verify installation
    sudo docker-compose --version
    log "Docker Compose installation completed"
}

stop_existing_container() {
    log "Checking for existing container"
    CONTAINER_ID=$(sudo docker ps -q -f name=daveved/little-daveved-explorer)
    if [ ! -z "$CONTAINER_ID" ]; then
        log "Stopping existing container $CONTAINER_ID"
        sudo docker stop $CONTAINER_ID
        sudo docker rm $CONTAINER_ID
        log "Existing container stopped and removed"
    else
        log "No existing container to stop"
    fi
}

deploy() {
    stop_existing_container
    sudo docker pull daveved/little-daveved-explorer
    sudo docker run -d -p 8001:8001 daveved/little-daveved-explorer
    log "Deployment completed"
}

# Main execution flow
install_docker
install_docker_compose
deploy

log "Deployment script execution completed"
