```json
{
  "id": "1kndmu8",
  "author": "trolleid",
  "category": "educational-story",
  "subreddit": "softwaredevelopment",
  "created_utc": 1747329096.0,
  "created_at": "2025-05-15T19:11:36+02:00",
  "permalink": "https://www.reddit.com/r/softwaredevelopment/comments/1kndmu8/eli5_http_authentication_basic_auth_bearer_auth/",
  "link_url": "https://www.reddit.com/r/softwaredevelopment/comments/1kndmu8/eli5_http_authentication_basic_auth_bearer_auth/",
  "is_self": true,
  "crosspost_parent": null,
  "removed_by_category": "automod_filtered",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "91f6d2446087e729fc3e3b0c1e1758757a84685174897bccfa2521287a9de973",
  "body_sha256": "0266568a7e128bbfcd1e94ccf3d42c0804da0f8ac36606e26fa8cad1b1b6f078",
  "body_characters": 7375
}
```

# Original title

ELI5: HTTP Authentication - Basic Auth, Bearer Auth and Cookie Auth

## Original body

This is a _super brief_ explanation of them which can serve as a quick-remembering-guide for example. I also mention some connected topics to keep in mind without going into detail and there's a short code snippet. Maybe helpful for someone :-) The repo is: https://github.com/LukasNiessen/http-authentication-explained

# HTTP Authentication: Simplest Overview

Basically there are 3 types: Basic Authentication, Bearer Authentication and Cookie Authentication.

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

## Which one to use?

Not Basic Authentication! 😄 So the question is: Bearer Auth or Cookie Auth?

They both have advantages and disadvantages. This is a topic for a separate article but I will quickly mention that bearer auth must be protected against XSS (Cross Site Scripting) and Cookie Auth must be protected against CSRF (Cross Site Request Forgery). You usually want to set your sensitive cookies to be Http Only. But again, this is a topic for another article.

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
```

## Example of Bearer Auth in Java

```java
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

```java
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
