ECHO Laboratory Work nr.5 - PKI

@REM SET HERE THE APPROPRIATE PATH TO PKI FOR YOU
SET PATH_TO_PKI=D:\Programming\Projects\CS-Laboratory-Works\Laboratory_Work_5_PKI_DSA\CA_Key_Cert
SET PATH_TO_OPENSSL=C:\Program Files\Git\usr\bin

ECHO Make directory for Private Key
MKDIR "%PATH_TO_PKI%"
C:
CD "%PATH_TO_OPENSSL%"
PAUSE
ECHO 1. Generate a private key using RSA Algorithm with 4096 bits
openssl genpkey -algorithm RSA -out "%PATH_TO_PKI%\ca_private_key.pem" -pkeyopt rsa_keygen_bits:4096

PAUSE

ECHO 2. Generate X509 Certificate for CA
@REM req - creates and processes certificate requests
@REM -new - generates a new certificate request
@REM -x509 - generates a self-signed certificate instead of a certificate request
@REM -days - specifies the number of days the certificate is valid
@REM -key - specifies the private key to use
@REM -out - specifies the file to write the certificate to Root CA Certificate
openssl req -new -x509 -noenc -days 3650 -key "%PATH_TO_PKI%\ca_private_key.pem" -out "%PATH_TO_PKI%\ca_root_cert.pem" 

PAUSE

ECHO 3. Display the content of the certificate
openssl x509 -in "%PATH_TO_PKI%\ca_root_cert.pem" -text -noout

PAUSE

ECHO 4. Generate a Private Key for the User
openssl genpkey -algorithm RSA -out "%PATH_TO_PKI%\user_private_key.pem" -pkeyopt rsa_keygen_bits:2048

PAUSE

ECHO 5. Generate a Certificate Signing Request for the User
@REM req - creates and processes certificate requests
@REM -new - generates a new certificate request
@REM -key - specifies the private key to use
@REM -out - specifies the file to write the certificate request to User Certificate Request
@REM in this case, the user is the one who wants to get a certificate from the CA
openssl req -new -key "%PATH_TO_PKI%\user_private_key.pem" -out "%PATH_TO_PKI%\user_cert_req.csr"

PAUSE

ECHO 6. Sign the User Certificate Request
@REM x509 - signs certificates
@REM -req - specifies the certificate request to sign
@REM -CA - specifies the CA certificate to use
@REM -CAkey - specifies the CA private key to use
@REM -CAcreateserial - creates a serial number file if it does not exist
@REM -out - specifies the file to write the certificate to User Certificate
@REM -days - specifies the number of days the certificate is valid
openssl x509 -req -in "%PATH_TO_PKI%\user_cert_req.csr" -CA "%PATH_TO_PKI%\ca_root_cert.pem" -CAkey "%PATH_TO_PKI%\ca_private_key.pem" -CAcreateserial -out "%PATH_TO_PKI%\user_cert.crt" -days 365

PAUSE

ECHO 7. Display the content of the certificate
openssl x509 -in "%PATH_TO_PKI%\user_cert.crt" -text -noout

PAUSE

ECHO 8. Sign a text file with the User Private Key
openssl dgst -sha256 -sign "%PATH_TO_PKI%\user_private_key.pem" -out "%PATH_TO_PKI%\signature.txt" "%PATH_TO_PKI%\user_text_to_be_signed.txt"

PAUSE

ECHO 9. Verify the signature

ECHO 9.1 Extract public key from the certificate
openssl x509 -in "%PATH_TO_PKI%\user_cert.crt" -pubkey -noout > "%PATH_TO_PKI%\public_key.pem"

ECHO 9.2 Verify the signature
openssl dgst -sha256 -verify "%PATH_TO_PKI%\public_key.pem" -signature "%PATH_TO_PKI%\signature.txt" "%PATH_TO_PKI%\user_text_to_be_signed.txt"

PAUSE

ECHO 10. Modify the text file
ECHO "This is a modified text file" > "%PATH_TO_PKI%\user_text_to_be_signed.txt"

PAUSE

ECHO 11. Verify the signature

ECHO 11.1 Extract public key from the certificate
openssl x509 -in "%PATH_TO_PKI%\user_cert.crt" -pubkey -noout > "%PATH_TO_PKI%\public_key.pem"

ECHO 11.2 Verify the signature
openssl dgst -sha256 -verify "%PATH_TO_PKI%\public_key.pem" -signature "%PATH_TO_PKI%\signature.txt" "%PATH_TO_PKI%\user_text_to_be_signed.txt"