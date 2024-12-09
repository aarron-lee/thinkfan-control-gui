#!/bin/bash

cp ./fan.py ./thinkfan

chmod +x ./thinkfan

sudo mv ./thinkfan /usr/local/bin/

sudo chcon -u system_u -r object_r --type=bin_t /usr/local/bin/thinkfan

sudo systemctl disable --now thinkfan.service

sudo cp ./thinkfan.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable --now thinkfan.service

echo "Install Complete"
