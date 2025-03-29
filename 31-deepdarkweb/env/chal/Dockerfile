FROM php:8.4.5-apache

# RUN apt-get -y update && \
#     apt-get -y --no-install-recommends install jq=1.6-2.1 && \
#     rm -rf /var/lib/apt/lists/* /var/cache/apt/*

COPY ./src /var/www/html

COPY ./000-default.conf /etc/apache2/sites-available/000-default.conf

RUN chown -R root:root /var/www && \
    find /var/www -type d -exec chmod 555 {} \; && \
    find /var/www -type f -exec chmod 444 {} \;

# TODO: Option Indexes

# RUN echo 'hkcert22{test_test_test}' > /flag && \
#     chown root:root /flag && chmod 555 /flag
