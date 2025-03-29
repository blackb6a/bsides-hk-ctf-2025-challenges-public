FROM php:8.4.5-apache-bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget mariadb-server mariadb-server supervisor && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli;

# add gosu for easy step-down from root
# https://github.com/tianon/gosu/releases
ENV GOSU_VERSION 1.17
RUN set -eux; \
	dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
	wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
	chmod +x /usr/local/bin/gosu; \
	gosu --version; \
	gosu nobody true

# Setup database
ARG MYSQL_ROOT_PASSWORD
ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
COPY --chown=root:root ./db/ /db/
RUN mkdir -p /docker-entrypoint-initdb.d && \
    cp /db/db.sql /docker-entrypoint-initdb.d && \
    mkdir -p /run/mysqld && \
    rm -rf /var/lib/mysql && \
	mkdir -p /var/lib/mysql /var/run/mysqld && \
	chown -R mysql:mysql /var/lib/mysql /var/run/mysqld && \
    find /etc/mysql/ -name '*.cnf' -print0 \
        | xargs -0 grep -lZE '^(bind-address|log|user\s)' \
        | xargs -rt -0 sed -Ei 's/^(bind-address|log|user\s)/#&/' && \
    chmod +x /db/database-init.sh && \
    /db/database-init.sh mysqld --version

# Setup apache webserver
COPY --chown=root:root php.ini /usr/local/etc/php/conf.d
COPY --chown=root:root 000-default.conf /etc/apache2/sites-available
COPY --chown=root:root ./html/ /var/www/html/
RUN sed -ri \
		-e 's!^(\s*CustomLog)\s+\S+!\1 /proc/self/fd/1!g' \
		-e 's!^(\s*ErrorLog)\s+\S+!\1 /proc/self/fd/2!g' \
		-e 's!^(\s*TransferLog)\s+\S+!\1 /proc/self/fd/1!g' \
		"/etc/apache2/apache2.conf" && \
    chown root:root -R /var/www/html && \
    chmod 755 /var/www/html && \
    chmod 1777 /var/www/html/u


# Start all components of the server
COPY --chown=root:root supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ARG FLAG
RUN echo "${FLAG}" > /flag_$(cat /dev/urandom | tr -dc '[:alnum:]' | head -c32)

WORKDIR /

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
