FROM bitk/pm_templater as build
COPY www.tpl dirlist.tpl ./
ARG PM_DOMAINS
ENV PM_DOMAINS ${PM_DOMAINS}
RUN ["python", "main.py", "www.tpl", "www.conf"]
RUN ["python", "main.py", "dirlist.tpl", "dirlist.txt"]

FROM nginx:1.19.0
RUN apt-get update && apt-get install -y nginx-extras
COPY handle_php.conf /etc/nginx/
COPY --from=build www.conf /etc/nginx/conf.d/
COPY --from=build dirlist.txt /
WORKDIR /var/www/html
RUN while read l; do \
        mkdir -p "$l/www" "$l/cors" "$l/public" "$l/unsafe"; \
        touch "$l/www/index.html" "$l/cors/index.html" "$l/public/index.html"  "$l/unsafe/index.html"; \
        done < /dirlist.txt;
CMD nginx -g "daemon off;"
