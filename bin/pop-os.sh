#!/bin/bash

task=pop-os

for dir in release proprietary; do
	rclone copy -v $task:$dir/ flow:$task/$dir
done
