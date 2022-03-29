#!/bin/bash

task=archlinux32

pool_list=(
	archisos
	pool
)

arch_list=(
	i486
	i686
	pentium4
)

repo_list=(
	build-support
	community-staging
	community-testing
	community
	core
	extra
	# gnome-unstable
	# kde-unstable
	staging
	testing
)

for dir in "${pool_list[@]}"; do
	rclone copy -v --http-no-head --ignore-existing arch:$task/$dir/ flow:$task/$dir
done

echo /$task/lastupdate > repo.list
for ext in {db,files}.tar.gz{,.old}; do
	for arch in "${arch_list[@]}"; do
		for repo in "${repo_list[@]}"; do
			echo /$task/$arch/$repo/$repo.$ext >> repo.list
		done
	done
	echo /$task/x86_64/releng/releng.$ext >> repo.list
done

rclone copy -v --no-traverse --files-from=repo.list arch: flow:

date +%s | rclone rcat flow:$task/lastsync
