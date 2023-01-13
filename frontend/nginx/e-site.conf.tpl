############################################################1
server {
    listen                  80;
    server_name             127.0.0.1;

    root                    /var/www/frontend/dist;

    access_log              /var/log/nginx/access.log combined buffer=512k flush=1m;
    error_log               /var/log/nginx/error.log warn;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://10.10.1.1:10100/;
    }

    # gzip
    gzip            on;
    gzip_vary       on;
    gzip_proxied    any;
    gzip_comp_level 6;
    gzip_types      text/plain text/css text/xml application/json application/javascript application/rss+xml application/atom+xml image/svg+xml;
}

############################################################2
server {
    listen                    443 ssl;
    server_name               formeta.space;

    root                      /var/www/frontend/dist;

    ssl_certificate           /etc/nginx/conf.d/cert/formeta.space.pem;
    ssl_certificate_key       /etc/nginx/conf.d/cert/formeta.space.key;
    ssl_session_timeout       5m;
    ssl_ciphers               ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols             TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://10.10.1.1:10100/;
    }

    # gzip
    gzip            on;
    gzip_vary       on;
    gzip_proxied    any;
    gzip_comp_level 6;
    gzip_types      text/plain text/css text/xml application/json application/javascript application/rss+xml application/atom+xml image/svg+xml;
}

server {
    listen           80;
    server_name      formeta.space;
    rewrite          ^(.*)$ https://$host$1;
}