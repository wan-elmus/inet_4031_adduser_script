#!/usr/bin/bash

for u in user04 user05 user06 user07 user08 user09; do
    sudo deluser --remove-home $u 2>/dev/null || true
    sudo delgroup $u 2>/dev/null || true
done