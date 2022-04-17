#!/bin/bash

task=pop-os

for dir in release proprietary; do
	rclone copy -v --http-no-head --ignore-existing --create-empty-src-dirs $task:$dir/ flow:$task/$dir
done
