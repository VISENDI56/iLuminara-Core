#!/bin/bash
# Modular installer for edge node
sudo apt-get update
sudo apt-get install -y docker.io python3-pip
sudo systemctl enable --now docker
pip3 install ansible
ansible-playbook playbooks/setup_edge_node.yaml
