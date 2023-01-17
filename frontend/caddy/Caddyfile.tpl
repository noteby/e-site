### Example-1
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

### Example-2
domain {
	encode zstd gzip

	handle {
		# Set this path to your site's directory.
		root * /root/dist

		# Enable the static file server.
		file_server

		try_files {path} /

		# Another common task is to set up a reverse proxy:
		# #reverse_proxy localhost:8080
	}

	handle_path /api/* {
		reverse_proxy 10.10.1.1:10100
	}

	log {
		output file /var/log/access.log
	}
}

### Example-3
domain {
	encode zstd gzip

	handle {
		# Set this path to your site's directory.
		root * /root/dist

		# Enable the static file server.
		file_server

		try_files {path} /

		# Another common task is to set up a reverse proxy:
		# #reverse_proxy localhost:8080
	}

	handle_path /api/* {
		reverse_proxy 10.10.1.1:10100
	}

	log {
		output file /var/log/caddy.log {
			roll_size 30MiB
			roll_keep 10
			roll_local_time
		}

		format filter {
			wrap json {
				time_format iso8601
				time_key time
				time_local
			}
			fields {
				user_id delete
			}
		}
	}
}
