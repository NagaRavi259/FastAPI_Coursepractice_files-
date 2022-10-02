# JSON Web TokenJWT (Token)
- JSON web token is a self-contained way to securly transmit data between two parties using a JSON object
- JSON web token can be trusted because each JWT can be digitally signed, which in return allows the server to know if the JWT has been changed at all
- JWT should be used when dealing with authorization
    - So client and user can be login securely
- JWT is a great way to exchange data between the server and client

## JSON web token (JWT) Structure
- A JSON web token is created of three seperate parts seperated by dots(.) Example:- aaaaaaa.bbbbbbb.ccccccccc
- which included:
    - Header:(a)
    - Payload:(b)
    - Signature:(c)

- ### Heder
    - A JWT Header usually consists of two parts:
        1. (alg) Algorithem for signing
        2. "type" specific type of token
    ``` 
            {
                "alg":"HS256"
                "typ":"JWT"
            }
    ```
    - the JWT Heder is then encoded using Base64to create the first part of the JWT(a)


- ### JWT Payload
    - A JWT payload consists  of the data. the payloads data contains claims, and there are three different types of cliams
        - Register
        - Public
        - Privite
    - The JWT Payload is then encoded using Base64 to create the second part of the JWT(b)
    ``` 
            {
                "sub":"12345678"
                "name":"name"
                "given_name":"given name"
                "family_name":"family name"
                "email":"test@email.com"
                "admin":true
            }
    ``` 
- JWT signature
    - A JWT Signature created by using the algorithem in the header to hash out the encoded header, encoded payload with a secret 
    - the secret can be anything, but is saved somewhere on the serer that client does not acess to 
    - The signature is the third and finale part of JWT(c)
    HMACSHA256(base64UrlEncode(Header)+"."+base64UrlEncode(Payload),secret)

- JSON Web Token string = eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiJhYmNkMTIzIiwiZXhwaXJ5IjoxNjQ2NjM1NjExMzAxfQ.3Thp81rDFrKXr3WrY1MyMnNK8kKoZBX9lg-JwFznR-M
- in the JWT token string we can observe each part was seperated by using the "."
- we can verify the JWT token on jwt website at https://jwt.io/

