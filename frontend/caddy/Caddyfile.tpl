domain {
	# Set this path to your site's directory.
	root * /root/dist

	# Enable the static file server.
	file_server

	# Another common task is to set up a reverse proxy:
	# reverse_proxy localhost:8080
	handle_path /api/* {
		reverse_proxy 10.10.1.1:10100
	}

	encode zstd gzip
}