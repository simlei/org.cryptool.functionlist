flist_dir_sandbox="$(realpath ${BASH_SOURCE[0]})"; flist_dir_sandbox="${flist_dir_sandbox%/*}"

export PYTHONPATH="$flist_dir_sandbox/src:$PYTHONPATH"
export PATH="$flist_dir_sandbox/bin:$PATH"
export PATH="$flist_dir_sandbox/src:$PATH"

export "${!flist_@}"

# vim: fdm=marker
