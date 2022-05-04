#!/bin/bash
set -emv
rclone copy --include=status.json --no-traverse flow: .
dumb $@ < status.json > modified.json
rclone copyto modified.json flow:status.json
