#! /bin/bash

sudo systemctl daemon-reload
sudo systemctl start myapi
sudo systemctl enable myapi
