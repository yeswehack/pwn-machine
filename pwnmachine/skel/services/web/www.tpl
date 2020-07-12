log_format  pm_log  '$time_local | $http_host $http_x_forwarded_for "$request" '
                  '$status "$http_referer" '
                  '"$http_user_agent"';

{% for domain in parse_json(PM_DOMAINS) %}
server {
    index index.php index.html;
    server_name {{domain}} www.{{domain}};
    error_log  /var/log/nginx/error.log;
    access_log /var/log/nginx/access.log pm_log;
    root /var/www/html/{{domain}}/www;
    
    include /etc/nginx/handle_php.conf;

    location = /favicon.ico {
      alias /var/www/html/favicon.png;
    }

}


server {
    index index.php index.html;
    server_name public.{{domain}};
    error_log  /var/log/nginx/error.log;
    access_log /var/log/nginx/access.log pm_log;
    root /var/www/html/public;
    
    location = /favicon.ico {
      alias /var/www/html/favicon.png;
    }

    include /etc/nginx/handle_php.conf;

    location / {
        autoindex on;
        autoindex_format html;
   }
}



server {
    index index.php index.html;
    server_name cors.{{domain}};
    error_log  /var/log/nginx/error.log;
    access_log /var/log/nginx/access.log pm_log;
    root /var/www/html/{{domain}}/cors;
    
    location = /favicon.ico {
      alias /var/www/html/favicon.png;
    }

    include /etc/nginx/handle_php.conf;

    location / {
        more_set_headers 'Access-Control-Allow-Origin: $http_origin';
        more_set_headers 'Access-Control-Allow-Methods: GET, POST, OPTIONS, PUT, DELETE, HEAD';
        more_set_headers 'Access-Control-Allow-Credentials: true';
        more_set_headers 'Access-Control-Allow-Headers: Origin,Content-Type,Accept,Authorization';

        if ($request_method = 'OPTIONS') {
            more_set_headers 'Access-Control-Allow-Origin: $http_origin';
            more_set_headers 'Access-Control-Allow-Methods: GET, POST, OPTIONS, PUT, DELETE, HEAD';
            more_set_headers 'Access-Control-Max-Age: 1728000';
            more_set_headers 'Access-Control-Allow-Credentials: true';
            more_set_headers 'Access-Control-Allow-Headers: *';
            more_set_headers 'Content-Type: text/plain; charset=UTF-8';
            more_set_headers 'Content-Length: 0';
            return 204;
        }
   }
}

server {
    index index.php index.html;
    server_name "~^(?<sub>.*)\.{{domain | regex_escape}}";
    error_log  /var/log/nginx/error.log;
    access_log /var/log/nginx/access.log pm_log;
    root /var/www/html/{{domain}}/$sub;

    location = /favicon.ico {
      alias /var/www/html/favicon.png;
    }
    
    include /etc/nginx/handle_php.conf;

    location /public/ {
        autoindex on;
        autoindex_format html;
    }
}

{% endfor %}
