---
title: "Overview of Authentication Methods: ELI5"
summary: "Simplest overview of Authentication Methods"
date: "June 16 2025"
draft: false
tags:
  - HTTP
  - Authentication
  - Basic Authentication
  - Bearer Authentication
  - Cookie Authentication
  - Certificate Authentication
---

# HTTP Authentication: Simplest Overview

Basically there are 3 types: Basic Authentication, Bearer Authentication and Cookie Authentication. I will give a _super brief_ explanation of them which can serve as a quick-remembering-guide for example. Besides that, I mention some connected topics to keep in mind without going into more detail and I have a quick code snippet as well.

## Basic Authentication

The simplest and oldest type - but it's insecure. So do not use it, just know about it.

It's been in HTTP since version 1 and simply includes the credentials in the request:

```
Authorization: Basic <base64(username:password)>
```

As you see, we set the HTTP header _Authorization_ to the string `username:password`, encode it with base64 and prefix `Basic`. The server then decodes the value, that is, remove `Basic` and decode base64, and then checks if the credentials are correct. **That's all**.

This is obviously insecure, even with HTTPS. If an attacker manages to 'crack' just one request, you're done.

Still, we need HTTPS when using Basic Authentication (eg. to protect against eaves dropping attacks). Small note: Basic Auth is also vulnerable to CSRF since the browser caches the credentials and sends them along subsequent requests automatically.

## Bearer Authentication

Bearer authentication relies on security tokens, often called bearer tokens. The idea behind the naming: the one bearing this token is allowed access.

Authorization: Bearer <token>

Here we set the HTTP header _Authorization_ to the token and prefix it with `Bearer`.

The token usually is either a JWT (JSON Web Token) or a session token. Both have advantages and disadvantages - I wrote a separate article about this.

Either way, if an attacker 'cracks' a request, he just has the token. While that is bad, usually the token expires after a while, rendering is useless. And, normally, tokens can be revoked if we figure out there was an attack.

We need HTTPS with Bearer Authentication (eg. to protect against eaves dropping attacks).

## Cookie Authentication

With cookie authentication we leverage cookies to authenticate the client. Upon successful login, the server responds with a Set-Cookie header containing a cookie name, value, and metadata like expiry time. For example:

```
Set-Cookie: JSESSIONID=abcde12345; Path=/
```

Then the client must include this cookie in subsequent requests via the _Cookie_ HTTP header:

```
Cookie: JSESSIONID=abcde12345
```

The cookie usually is a token, again, usually a JWT or a session token.

We need to use HTTPS here.

## API Key Authentication

API Keys are like permanent passwords for your API. Super simple - you just include a key in your request, either as a header:

```
X-API-Key: abcd1234567890
```

Or sometimes as a URL parameter:

```
GET /api/data?api_key=abcd1234567890
```

The server checks if the key exists in its database and if it has the right permissions. That's it.

The problem? If someone steals your API key, they can use it until you notice and revoke it. Unlike tokens, API keys typically don't expire. Also, putting keys in URLs (query params) is risky - they show up in logs, browser history, etc.

Here you always need to use HTTPS and prefer headers over query parameters for API keys.

## Certificate-Based Authentication (CBA)

Usually we are talking about X.509 certificates. Much simplified, they are just structured X.509 files that include information, such as subject (who you are), a public key, your issuer (who vouched for you), when it starts and expires and more. This certificate is not a secret, it's public information, including the public key.

It's much more nuanced, but here a simple example of how it works:

1. Client presents its certificate (public part) to the server.
2. Server sends a challenge (part of the TLS handshake) that must be signed by the private key corresponding to that certificate.
3. Client signs the challenge using its private key.
4. Server verifies the signature using the certificate’s public key.
5. If the signature matches, the server knows the client owns the private key → authentication succeeds.

Important note: this happens during the TLS handshake, that is, it happens at the transport layer (4th layer in the OSI model). So the certificate is not sent in any HTTP request (that would be layer 7).

mTLS (mutual TLS) is a special type of CBA, here both client and server authenticate each other, both via certificates.

## Digest Authentication
Think of this as Basic Auth's smarter sibling. Instead of sending the password directly, we send a hash (digest) of it.

```
Authorization: Digest username="demo", realm="api", nonce="dcd98b7102dd2f0e8b11d0f600bfb0c093", response="6629fae49393a05397450978507c4ef1"
```

The server sends a challenge with a nonce (random value), the client creates a hash using the password, nonce, and other values, then sends it back. The server does the same calculation and compares.

Better than Basic? Yes. Worth using today? Not really. Bearer tokens are simpler and more flexible.

## OAuth 2.0 (Special Mention)

OAuth 2.0 isn't really an authentication method - it's an authorization framework. But it's so common, we should mention it. It typically uses Bearer tokens under the hood.

The flow usually goes:

```
1. Your app redirects user to provider (Google, Facebook, etc.)
2. User logs in there and approves permissions
3. Provider redirects back with an authorization code
4. Your app exchanges the code for an access token
5. Use the token as a Bearer token
```

Note that if we do step 5, this is called OIDC. More info on OAuth 2.0 [here](https://lukasniessen.com/blog/101-oauth-explained/), more on OIDC [here](https://lukasniessen.com/blog/102-oidc-explained/).

## Which one to use?

Not Basic Authentication! 😄

They all have advantages and disadvantages. This is a topic for a separate article but I will quickly mention that bearer auth must be protected against XSS (Cross Site Scripting) and Cookie Auth must be protected against CSRF (Cross Site Request Forgery). You usually want to set your sensitive cookies to be Http Only. But again, this is a topic for another article.

## Example of Basic Auth in Java

```Java
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class BasicAuthClient {
    public static void main(String[] args) {
        try {
            String username = "demo";
            String password = "p@55w0rd";
            String credentials = username + ":" + password;
            String encodedCredentials = Base64.getEncoder()
                .encodeToString(credentials.getBytes(StandardCharsets.UTF_8));

            URL url = new URL("https://api.example.com/protected");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Authorization", "Basic " + encodedCredentials);

            int responseCode = conn.getResponseCode();
            System.out.println("Response Code: " + responseCode);

            if (responseCode == 200) {
                System.out.println("Success! Access granted.");
            } else {
                System.out.println("Failed. Check credentials or endpoint.");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

## Example of Bearer Auth in Java

```Java
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class BearerAuthClient {
    public static void main(String[] args) {
        try {
            String token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."; // Replace with your token
            URL url = new URL("https://api.example.com/protected-resource");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Authorization", "Bearer " + token);

            int responseCode = conn.getResponseCode();
            System.out.println("Response Code: " + responseCode);

            if (responseCode == 200) {
                System.out.println("Access granted! Token worked.");
            } else {
                System.out.println("Failed. Check token or endpoint.");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

## Example of Cookie Auth in Java

```Java
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

public class CookieAuthClient {
    public static void main(String[] args) {
        try {
            // Step 1: Login to get session cookie
            URL loginUrl = new URL("https://example.com/login");
            HttpURLConnection loginConn = (HttpURLConnection) loginUrl.openConnection();
            loginConn.setRequestMethod("POST");
            loginConn.setDoOutput(true);
            loginConn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");

            String postData = "username=demo&password=p@55w0rd";
            try (OutputStream os = loginConn.getOutputStream()) {
                os.write(postData.getBytes(StandardCharsets.UTF_8));
            }

            String cookie = loginConn.getHeaderField("Set-Cookie");
            if (cookie == null) {
                System.out.println("No cookie received. Login failed.");
                return;
            }
            System.out.println("Received cookie: " + cookie);

            // Step 2: Use cookie for protected request
            URL protectedUrl = new URL("https://example.com/protected");
            HttpURLConnection protectedConn = (HttpURLConnection) protectedUrl.openConnection();
            protectedConn.setRequestMethod("GET");
            protectedConn.setRequestProperty("Cookie", cookie);

            int responseCode = protectedConn.getResponseCode();
            System.out.println("Response Code: " + responseCode);

            if (responseCode == 200) {
                System.out.println("Success! Session cookie worked.");
            } else {
                System.out.println("Failed. Check cookie or endpoint.");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

## Example of API Key Auth in Java

```Java
import java.net.HttpURLConnection;
import java.net.URL;

public class ApiKeyAuthClient {
    public static void main(String[] args) {
        try {
            String apiKey = "sk_live_1234567890abcdef"; // Your API key
            
            // Using header (preferred)
            URL url = new URL("https://api.example.com/data");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("X-API-Key", apiKey);
            
            // Alternative: Using query parameter (less secure)
            // URL url = new URL("https://api.example.com/data?api_key=" + apiKey);
            
            int responseCode = conn.getResponseCode();
            System.out.println("Response Code: " + responseCode);
            
            if (responseCode == 200) {
                System.out.println("Success! API key accepted.");
            } else if (responseCode == 401) {
                System.out.println("Invalid API key.");
            } else {
                System.out.println("Failed. Check key or endpoint.");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

## Example of Certificate-Based Auth in Java

```Java
import javax.net.ssl.*;
import java.io.FileInputStream;
import java.net.URL;
import java.security.KeyStore;

public class CertificateAuthClient {
    public static void main(String[] args) {
        try {
            // Load client certificate
            KeyStore keyStore = KeyStore.getInstance("PKCS12");
            keyStore.load(new FileInputStream("client-cert.p12"), "password".toCharArray());
            
            KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
            kmf.init(keyStore, "password".toCharArray());
            
            // Load trusted certificates
            KeyStore trustStore = KeyStore.getInstance("JKS");
            trustStore.load(new FileInputStream("truststore.jks"), "truststorepass".toCharArray());
            
            TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
            tmf.init(trustStore);
            
            // Setup SSL context with both client cert and trust store
            SSLContext sslContext = SSLContext.getInstance("TLS");
            sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);
            
            // Make the request
            URL url = new URL("https://secure-api.example.com/data");
            HttpsURLConnection conn = (HttpsURLConnection) url.openConnection();
            conn.setSSLSocketFactory(sslContext.getSocketFactory());
            conn.setRequestMethod("GET");
            
            int responseCode = conn.getResponseCode();
            System.out.println("Response Code: " + responseCode);
            
            if (responseCode == 200) {
                System.out.println("Success! Certificate authenticated.");
            } else {
                System.out.println("Failed. Check certificate or permissions.");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```