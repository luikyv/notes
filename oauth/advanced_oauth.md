# Advanced OAuth

## PKCE - Proof Key for Code Exchange
PKCE is an extension of the OAuth framework that prevents attacks such as authorization code injection. By using PKCE, the authorization server guarantees that the client that started the flow is the same that requests the access token.

## PAR - Pushed Authorization Request
When the client wants to start an authorization flow, instead of building the /authorize URL with all the information exposed, it sends the information through the back channel using the /par endpoint. By doing so, the flow is started in the back channel and sensitive information will not be exposed.


## Private Key JWT
The client authenticates itself by signing a JWT with its private key. The corresponding public key is registed in the authorization server so it can verify the signature.

The client signs a JWT that has a payload as following one:
```json
{
    "sub": "CLIENT_ID",
    "iss": "CLIENT_ID",
    "aud": "https://authorization-server.com/",
    "nbf": "1690675915",
    "iat": "1690675915",
    "exp": "1690676915"
}
```

## Sender-Constraining Tokens
A sender-constraining token can only be used by the party the token was issued to. To do so, the client using the token must be authenticated somehow.

### MTLS - Mutual TLS
During normal TLS, only the server presents a certificate, whereas in MTLS, the client must present its certificate as well. Other than being used to authenticate clients, MTLS can be used to implementing sender-constraining tokens.

Since the client presents its certificate, we can add more security to the framework by binding the access token to the client's certificate. In that case, resource servers must also support MTLS in order to validate tokens.

One way of binding certificates to JWT access tokens is by adding a claim to the token with the hash of the certificate:
```json
{
    "cnf": {
        "x5t#S256": "asdu8fu8oiq4jriojoifausd8f"
    }
}
```

### DPoP - Demonstration of Proof-of-Possesion
The big issue with MTLS is that it requires modifying the transport layer. DPoP, in turn, happens in the application layer, therefore it is easier to implement. However, DPoP doesn't provide a way to authenticate clients which is the case for MTLS.