```json
{
  "id": "1kne5et",
  "author": "trolleid",
  "category": "educational-story",
  "subreddit": "angularjs",
  "created_utc": 1747330317.0,
  "created_at": "2025-05-15T19:31:57+02:00",
  "permalink": "https://www.reddit.com/r/angularjs/comments/1kne5et/eli5_basic_auth_bearer_auth_and_cookie_auth/",
  "link_url": "https://www.reddit.com/r/angularjs/comments/1kne5et/eli5_basic_auth_bearer_auth_and_cookie_auth/",
  "is_self": true,
  "crosspost_parent": null,
  "removed_by_category": "reddit",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "ff07ecf7ce4231818259034386d421e4c51fed75dab69aac833bc3b82314e5b1",
  "body_sha256": "cee6607397867453ac3172758c713d2893fcc4a639f8d1630fe1b4a3346131d1",
  "body_characters": 6407
}
```

# Original title

ELI5: Basic Auth, Bearer Auth and Cookie Auth

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

```TypeScript
const basicAuthRequest = async (): Promise<void> => {
    try {
        const username: string = "demo";
        const password: string = "p@55w0rd";
        const credentials: string = `${username}:${password}`;
        const encodedCredentials: string = btoa(credentials);

        const response: Response = await fetch("https://api.example.com/protected", {
            method: "GET",
            headers: {
                "Authorization": `Basic ${encodedCredentials}`,
            },
        });

        console.log(`Response Code: ${response.status}`);

        if (response.ok) {
            console.log("Success! Access granted.");
        } else {
            console.log("Failed. Check credentials or endpoint.");
        }
    } catch (error) {
        console.error("Error:", error);
    }
};

// Execute the function
basicAuthRequest();
```

## Example of Bearer Auth in Java

```TypeScript
const bearerAuthRequest = async (): Promise<void> => {
    try {
        const token: string = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."; // Replace with your token

        const response: Response = await fetch("https://api.example.com/protected-resource", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        });

        console.log(`Response Code: ${response.status}`);

        if (response.ok) {
            console.log("Access granted! Token worked.");
        } else {
            console.log("Failed. Check token or endpoint.");
        }
    } catch (error) {
        console.error("Error:", error);
    }
};

// Execute the function
bearerAuthRequest();
```

## Example of Cookie Auth in Java

```TypeScript
const cookieAuthRequest = async (): Promise<void> => {
    try {
        // Step 1: Login to get session cookie
        const loginData: URLSearchParams = new URLSearchParams({
            username: "demo",
            password: "p@55w0rd",
        });

        const loginResponse: Response = await fetch("https://example.com/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: loginData.toString(),
            credentials: "include", // Include cookies in the request
        });

        const cookie: string | null = loginResponse.headers.get("Set-Cookie");
        if (!cookie) {
            console.log("No cookie received. Login failed.");
            return;
        }
        console.log(`Received cookie: ${cookie}`);

        // Step 2: Use cookie for protected request
        const protectedResponse: Response = await fetch("https://example.com/protected", {
            method: "GET",
            headers: {
                "Cookie": cookie,
            },
            credentials: "include", // Ensure cookies are sent
        });

        console.log(`Response Code: ${protectedResponse.status}`);

        if (protectedResponse.ok) {
            console.log("Success! Session cookie worked.");
        } else {
            console.log("Failed. Check cookie or endpoint.");
        }
    } catch (error) {
        console.error("Error:", error);
    }
};

// Execute the function
cookieAuthRequest();
```
