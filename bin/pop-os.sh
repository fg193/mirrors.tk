#!/bin/bash
set -v


task=pop-os

dumb.sh syncing $task 0 ${interval:=24h}

for dir in release proprietary staging/master staging-proprietary; do
	rclone copy $task:$dir/pool/  flow:$task/$dir/pool  -v --transfers=1 --stats-file-name-length=0 --http-no-head --ignore-existing
	rclone copy $task:$dir/dists/ flow:$task/$dir/dists -v --transfers=1 --stats-file-name-length=0
done

dumb.sh success $task $(size.sh flow:$task)


task=pop-iso

dumb.sh syncing $task 0 ${interval}

pop-iso.py > $task.list
rclone copy $task: flow:$task -v --files-from $task.list --no-traverse --transfers=1 --stats-file-name-length=0 --http-no-head --ignore-existing

dumb.sh success $task $(size.sh flow:$task)
