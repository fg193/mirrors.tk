#!/bin/sh
rclone size --json -q $@ | python3 -c 'print(__import__("json").loads(input())["bytes"])'
