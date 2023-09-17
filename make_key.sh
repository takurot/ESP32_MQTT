# CAの証明書とプライベートキーを生成
openssl req -new -x509 -days 365 -extensions v3_ca -keyout ca.key -out ca.crt

# サーバーの鍵を生成
openssl genrsa -out server.key 2048

# サーバーの証明書要求(CSR)を生成
openssl req -new -out server.csr -key server.key

# CSRを使用してサーバーの証明書を生成
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365
