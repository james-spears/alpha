openssl req -newkey rsa:2048 \
  -new -nodes -x509 \
  -days 3650 \
  -out cert.pem \
  -keyout key.pem \
  -subj "/C=CA/ST=Ontario/L=Toronto/O=alpha/OU=Node/CN=crypto" \
  -config "./ssl.conf"