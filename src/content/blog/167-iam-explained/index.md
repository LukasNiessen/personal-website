---
title: "IAM: Everything You Need to Know"
summary: "The full picture of Identity and Access Management - from login flows and tokens to backend validation and client-side storage"
date: "Apr 12 2026"
tags:
  - IAM
  - Security
  - Authentication
  - Authorization
  - OAuth
  - OIDC
  - JWT
---

# IAM: Everything You Need to Know

You click "Login with Google," type your password, and you're in. Behind that one click there's a whole world of redirects, tokens, cryptographic signatures, and platform integrations working together. This article walks through the entire Identity and Access Management (IAM) picture, end to end. From the moment a user hits "Login" on a website, through what happens on the IAM platform, down to how the backend validates the token it receives.

I'll focus primarily on web applications (things running in the browser), but I'll also address how it works for Electron apps and native apps. And I'll keep it modern - the gold standard today is OIDC on top of OAuth 2.0, and that's what we'll look at.

## The Big Picture

Before diving into details, here's the full flow at a glance:

```
┌──────────────┐      ┌──────────────────┐      ┌──────────────────┐
│              │      │                  │      │                  │
│   Client     │─────►│   IAM Platform   │─────►│ Identity Provider│
│  (Browser,   │◄─────│  (Keycloak,      │◄─────│  (Google, Apple, │
│   App, etc.) │      │   Okta, Auth0)   │      │   Entra ID)      │
│              │      │                  │      │                  │
└──────┬───────┘      └──────────────────┘      └──────────────────┘
       │
       │  Token (JWT)
       │
       ▼
┌──────────────┐      ┌──────────────────┐
│              │      │                  │
│   Backend    │─────►│  JWKS Endpoint   │
│   (API)      │      │  (Public Keys)   │
│              │      │                  │
└──────────────┘      └──────────────────┘
```

1. The **client** (your website, app, whatever) redirects the user to the **IAM platform**
2. The IAM platform handles login, either directly or by redirecting further to an **identity provider**
3. After successful authentication, the IAM platform issues **tokens** (typically JWTs) back to the client
4. The client stores these tokens and sends them along with every request to the **backend**
5. The backend **validates** the tokens using the IAM platform's public keys (JWKS)
6. If valid, the backend knows who the user is and can make **authorization** decisions

That's the skeleton. Let's flesh it out.

## The IAM Platform

The IAM platform is the central piece that manages your users, their credentials, and the login experience. Think of it as the thing that sits between your app and the actual identity verification.

Popular options include:

- **Keycloak** - Open source, self-hosted. Very common in enterprise environments
- **Okta** / **Auth0** - Auth0 is now part of Okta. Cloud-hosted, managed service
- **AWS Cognito** - AWS's IAM offering
- **Azure AD B2C** / **Microsoft Entra ID** - Microsoft's solutions
- **Firebase Authentication** - Google's managed auth for smaller apps

What you configure in these platforms is essentially:

- **Which identity providers** are allowed (Google, Apple, Microsoft, etc.)
- **What scopes and claims** are included in tokens
- **Token lifetimes** (how long access tokens and refresh tokens are valid)
- **Client applications** (which apps are allowed to authenticate through this platform)
- **User roles and permissions** (for authorization)
- **Branding** (the login page look and feel)

The IAM platform also provides a **hosted login page**. This is important. Instead of building your own login form, the standard approach is to redirect users to the IAM platform's hosted page. This way, your application never touches user credentials. The user authenticates directly with the IAM platform (or with an identity provider through it), and your app only receives tokens.

## Identity Providers

Identity providers (IdPs) are the services that actually verify who a user is. When you click "Login with Google," Google is the identity provider. Common ones:

- **Google Identity**
- **Apple Sign-In**
- **Microsoft Entra ID** (formerly Azure AD)
- **GitHub**
- **Facebook**

Your IAM platform connects to these via OIDC (OpenID Connect). You register your IAM platform as a client with each IdP you want to support, and the IAM platform handles the back-and-forth.

You can also have users log in directly with credentials (email + password) managed by the IAM platform itself, without any external IdP. Most IAM platforms support both.

## The Authentication Flow: OIDC + OAuth 2.0

The gold standard protocol for all of this is **OIDC (OpenID Connect)** built on top of **OAuth 2.0**. In short:

- **OAuth 2.0** is an authorization protocol. It was designed so that third-party apps can access resources on behalf of a user without knowing the user's password
- **OIDC** extends OAuth 2.0 with an authentication layer. It adds the concept of an ID token that tells your app _who_ the user is

I've written detailed guides on both of these: [OAuth explained](/blog/101-oauth-explained) and [OIDC explained](/blog/102-oidc-explained). I'll keep it brief here and focus on how they fit into the full IAM picture.

### The Redirect Dance

Here's what happens when a user clicks "Login" on your web app:

1. Your app redirects the user to the IAM platform's **authorization endpoint**
   - The URL includes your `client_id`, a `redirect_uri`, requested `scopes` (like `openid profile email`), and a `state` parameter for CSRF protection
2. The IAM platform shows its **hosted login page**
   - The user can log in with credentials directly, or click "Login with Google" (or whatever IdPs are configured)
3. If the user picks an external IdP, the IAM platform redirects them again to that **IdP's login page** (e.g., Google's consent screen)
4. The user authenticates with the IdP
5. The IdP redirects back to the **IAM platform** with an authorization code
6. The IAM platform exchanges that code with the IdP for user info
7. The IAM platform now knows who the user is. It generates its own tokens and redirects back to **your app** with an authorization code
8. Your app exchanges that code (server-to-server) for the actual tokens: an **access token**, an **ID token** (JWT), and usually a **refresh token**

Why the authorization code? Why not just send the tokens directly? Because the redirect happens through the user's browser, and we don't want tokens floating around in browser URLs. The code-to-token exchange happens server-to-server, where the `client_secret` is included. This proves to the IAM platform that the requester is actually your app, not someone who intercepted the code. (More detail on this in my [OAuth article](/blog/101-oauth-explained).)

## Tokens

After the flow completes, your app has three tokens. Let's be clear about what each one does.

### Access Token

The access token is what your app sends to the backend API on every request. It's a credential that says "the user authorized this app to do X." It's usually short-lived (minutes to an hour).

The access token can be a JWT, but it doesn't have to be. Some IAM platforms issue opaque access tokens (just a random string) that the backend has to validate by calling the IAM platform's introspection endpoint. But JWTs are more common because they can be validated locally.

### ID Token

The ID token is always a JWT. It contains claims about the user's identity: who they are (`sub`), their name, email, etc. This is the OIDC addition to OAuth 2.0. Your frontend can decode this to display the user's name and profile picture without making another API call.

Important: the ID token is for the **client** (your frontend). Don't send it to your backend API as an authorization credential. Use the access token for that.

### Refresh Token

The refresh token is long-lived (days, weeks, or even months). When the access token expires, your app uses the refresh token to get a new access token without forcing the user to log in again. The refresh token is exchanged server-to-server (or, for public clients like SPAs, via a secure backchannel).

This is why you can close a tab, come back hours later, and still be logged in. The access token expired, but the refresh token is still valid, so the app silently gets a new access token.

### Quick Note on JWT Structure

A JWT has three parts separated by dots: `header.payload.signature`

```
eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ikx1a2FzIn0.signature_here
```

- **Header**: Algorithm used for signing (e.g., RS256) and token type
- **Payload**: The claims - `sub` (user ID), `iss` (issuer), `exp` (expiration), `aud` (audience), plus custom claims like roles
- **Signature**: The cryptographic proof that this token was issued by who it claims and hasn't been tampered with

The header and payload are just Base64-encoded JSON. Anyone can decode them. The signature is what makes it secure. To understand how, we need to talk about JWKS.

## JWKS and Asymmetric Cryptography

This is one of those things that sounds complex but is actually quite elegant once you get it.

### The Problem

Your backend receives a JWT from a client. It needs to verify that this token was actually issued by the IAM platform and hasn't been tampered with. But the backend can't just call the IAM platform for every single request, that would be too slow and would create a single point of failure.

### The Solution: Asymmetric Cryptography

Asymmetric cryptography (also called public-key cryptography) uses a **key pair**: a private key and a public key.

- The **private key** is kept secret by the IAM platform. It uses this key to **sign** every JWT it issues
- The **public key** is, well, public. Anyone can have it. It can only be used to **verify** signatures, not create them

This is the critical insight: knowing the public key lets you verify that a token was signed by the private key, but it does not let you create new tokens. So the IAM platform publishes its public keys, and any backend service can verify tokens independently, without ever needing to talk to the IAM platform in real time.

### How Signing Works

When the IAM platform creates a JWT:

1. It takes the header and payload, combines them
2. It runs a cryptographic signing algorithm (e.g., RSA with SHA-256, hence "RS256") using its **private key**
3. The result is the signature, the third part of the JWT

When your backend receives a JWT:

1. It takes the header and payload from the token
2. It uses the **public key** to verify the signature
3. If the verification passes, the token is authentic and untampered

If someone changed even a single character in the payload (say, changed the user's role from "user" to "admin"), the signature would no longer match. And they can't create a new valid signature because they don't have the private key.

### The JWKS Endpoint

JWKS stands for JSON Web Key Set. It's simply a URL endpoint that the IAM platform exposes, which returns its public keys in a standardized JSON format.

For example, Google's JWKS endpoint is:
`https://www.googleapis.com/oauth2/v3/certs`

Your backend typically fetches these keys once (and caches them), then uses them to validate all incoming JWTs. The keys do rotate periodically, so your backend should re-fetch them when it encounters a `kid` (Key ID) in a JWT header that it doesn't recognize.

The JWKS response looks something like this:

```json
{
  "keys": [
    {
      "kty": "RSA",
      "kid": "abc123",
      "use": "sig",
      "n": "0vx7agoebGc...",
      "e": "AQAB"
    }
  ]
}
```

The `n` and `e` values are the RSA public key components. Libraries like `jsonwebtoken` or `jose` handle all of this for you.

### OIDC Discovery

You don't even need to hardcode the JWKS endpoint URL. OIDC defines a **discovery document** at a well-known URL:

`https://<issuer>/.well-known/openid-configuration`

This JSON document contains the URLs for the authorization endpoint, token endpoint, JWKS endpoint, supported scopes, and more. Your backend (or frontend) can fetch this once and dynamically discover everything it needs.

## Where Tokens Live: Client-Side Storage

This is where things get platform-specific. The tokens need to be stored somewhere on the client so they can be sent with every request to the backend. Let's go through the options.

### Web Applications (Browser)

For web apps, you have four main options. Each has trade-offs.

**Cookies (httpOnly, Secure, SameSite)**

The backend sets the token in an `httpOnly` cookie. The browser automatically sends it with every request to that domain. The frontend JavaScript cannot read the cookie at all (`httpOnly` prevents that), which is a big security win against XSS attacks.

- Sent automatically with every request (no code needed)
- `httpOnly` protects against XSS (JavaScript can't access the token)
- `Secure` ensures it's only sent over HTTPS
- `SameSite` attribute helps prevent CSRF attacks
- Works out of the box for same-domain setups

The downside: cookies are domain-bound. If your API is on a different domain than your frontend, you need to deal with CORS and cross-origin cookie settings, which gets messy. Also, cookies are automatically sent with _every_ request to that domain, including navigation requests, image loads, etc. That's unnecessary overhead in some cases.

**localStorage**

Store the token in `localStorage`. You manually attach it as a `Bearer` token in the `Authorization` header for every API call.

- Persistent across browser sessions (survives tab close)
- Simple to use
- Works regardless of API domain (just set the header)

The downside: `localStorage` is accessible to any JavaScript running on your page. If you have an XSS vulnerability, an attacker can steal the token. This is the main argument against `localStorage` for tokens.

**sessionStorage**

Like `localStorage`, but the token is cleared when the tab or browser is closed.

- Slightly safer than `localStorage` (shorter exposure window)
- Token doesn't persist across sessions

The downside: same XSS vulnerability as `localStorage`. And the user has to re-authenticate every time they close the browser, which is usually bad UX.

**In-Memory (e.g., a JavaScript variable, React state, Redux store)**

Store the token only in a JavaScript variable. It's never persisted to disk at all.

- Most secure against token theft (nothing stored that survives a page refresh)
- XSS can still read it while the page is open, but can't steal a persisted copy

The downside: the token is gone on page refresh. So you need a way to get it back, usually via a refresh token stored in an `httpOnly` cookie. This is actually the pattern many modern SPAs use: the access token lives in memory, and the refresh token lives in a secure cookie. On page load, the app uses the refresh token to silently obtain a new access token.

**The modern recommendation** for SPAs is typically: access token in memory, refresh token in a secure `httpOnly` cookie. Some teams go further and use the Backend-for-Frontend (BFF) pattern, where a thin backend handles all token management and the browser only ever receives a session cookie. This keeps tokens completely out of the browser.

### Electron Apps

Electron is interesting because it's basically a Chromium browser bundled with Node.js. So yes, Electron apps do have access to cookies, `localStorage`, and `sessionStorage`, just like a regular browser.

However, Electron apps also have access to Node.js APIs and the operating system. This means they can use **OS-level secure storage**:

- **Windows**: Credential Manager (via the `keytar` library or Electron's `safeStorage` API)
- **macOS**: Keychain
- **Linux**: Secret Service API (e.g., GNOME Keyring)

So for apps like Microsoft Teams, Slack, or VS Code, the typical approach is to use the OS-level secure storage for refresh tokens and keep access tokens in memory. This is more secure than `localStorage` because the OS-level storage is encrypted and not accessible to other applications or browser-like XSS attacks.

The authentication flow itself usually works via the system browser or an embedded browser view: the app opens a login window, the OIDC redirect dance happens, and the token comes back to the app via a custom protocol handler or localhost redirect.

### Native Apps (Android, iOS, Windows)

The principle is exactly the same: authenticate via OIDC, receive tokens, store them securely, send them with requests. What differs is the storage mechanism.

**Android**: Use the **Android Keystore** system. It's hardware-backed on most modern devices, meaning the keys are stored in a secure hardware module that even a rooted device can't easily extract from. For the login flow, use `AppAuth` (an open-source library) which opens the system browser for authentication.

**iOS**: Use the **Keychain**. Similar to Android Keystore, it's the OS-provided secure storage. For the login flow, use `ASWebAuthenticationSession` which handles the OIDC redirect in a secure browser session.

**Windows (native)**: Use the **Windows Credential Manager** or **DPAPI** for token storage. For the login flow, libraries like MSAL (Microsoft Authentication Library) handle the browser-based OIDC flow.

In all cases, the pattern is:
1. Open a secure browser session for OIDC login
2. Receive tokens via redirect
3. Store the refresh token in OS-level secure storage
4. Keep the access token in memory
5. Attach the access token to API requests (typically as a `Bearer` token in the `Authorization` header)

So yes, as you can see, the concept is the same everywhere. The only thing that changes is _where_ you store the tokens and _how_ the redirect callback works on each platform.

## How the Backend Validates Tokens

Your backend receives a request with a token. Now what?

### Step 1: Extract the Token

The token arrives either as:
- A **Bearer token** in the `Authorization` header: `Authorization: Bearer eyJhbGci...`
- An **httpOnly cookie** (automatically sent by the browser)

### Step 2: Validate the JWT

The backend needs to:

1. **Decode the JWT header** to get the `kid` (Key ID) and `alg` (algorithm)
2. **Look up the public key** from the cached JWKS that matches the `kid`
3. **Verify the signature** using that public key
4. **Check the claims**:
   - `iss` (issuer) - matches your IAM platform's URL
   - `aud` (audience) - matches your application's client ID
   - `exp` (expiration) - token hasn't expired
   - `nbf` (not before) - token is already valid
   - Any custom claims you need (roles, permissions, etc.)

If all of this checks out, the user is **authenticated**. You know who they are (from the `sub` claim) and that the IAM platform vouches for them.

### Step 3: Authorization

Authentication tells you _who_ the user is. Authorization tells you _what they're allowed to do_. These are different things.

After validating the token, the backend checks whether the authenticated user has permission to perform the requested action. This can be based on:

- **Roles** in the JWT claims (e.g., `"roles": ["admin", "editor"]`)
- **Scopes** in the JWT (e.g., `"scope": "read:articles write:articles"`)
- **Database lookups** (check a permissions table for finer-grained access)
- **Policy engines** like OPA (Open Policy Agent) for complex authorization logic

The level of complexity here depends entirely on your application. A simple blog might just check if you're an admin. A multi-tenant SaaS with fine-grained permissions might need a full policy engine.

## Cookie vs Bearer Token vs Session Token

These terms get thrown around a lot, and they overlap in confusing ways. Let me clarify.

### Session Token (Server-Side Sessions)

The traditional approach. The server creates a session (stored in memory, a database, or Redis), generates a random session ID, and sends that ID to the client as a cookie. On every request, the server looks up the session by its ID.

- The token itself is meaningless (just a random string), all data lives on the server
- Server needs to store and look up session data for every request
- Scales poorly in distributed systems (you need sticky sessions or a shared session store)
- Simple and battle-tested

### Bearer Token (JWT)

The modern approach. The token itself contains the data (user ID, roles, expiration). The server doesn't need to store anything.

- Stateless: no server-side storage needed
- Scales easily in distributed systems (any server can validate the token independently)
- Larger than session IDs (JWTs can be several hundred bytes)
- Can't be easily revoked (the token is valid until it expires, unless you maintain a blacklist)

### Cookie

Here's the thing: **a cookie is a transport mechanism, not a token type**. You can put a session ID in a cookie. You can put a JWT in a cookie. The cookie is just how the browser stores and sends the value.

So "cookie vs bearer token" is a misleading comparison. The real question is:

1. **Session-based auth** (random session ID, server stores the state) vs. **token-based auth** (JWT, client stores the state)
2. **Cookie transport** (browser sends it automatically) vs. **Authorization header** (your code sends it manually)

You can actually mix and match: JWT stored in an `httpOnly` cookie is a common and solid pattern. You get the statelessness of JWTs with the XSS protection of `httpOnly` cookies.

### What's Most Common Today?

For **SPAs and modern web apps**: Token-based auth with JWTs. Access token in memory or `Authorization` header, refresh token in an `httpOnly` cookie. Or the BFF pattern.

For **traditional server-rendered apps**: Session-based auth with a session cookie. Still works great, no need to over-engineer it.

For **mobile and native apps**: Token-based auth with JWTs, stored in OS-level secure storage. Bearer token in the `Authorization` header.

For **microservices communicating with each other**: JWTs or mutual TLS (mTLS). Often, the API gateway validates the JWT once and passes verified claims to downstream services.

## TLS: The Foundation of It All

One thing I want to mention briefly: all of this relies on HTTPS being in place. TLS (Transport Layer Security) encrypts the communication between client and server, so tokens can't be intercepted in transit.

Without HTTPS, it doesn't matter how sophisticated your token strategy is. Anyone on the network could just read the token. This is why OIDC requires HTTPS, and why OAuth 2.0 delegates its security to TLS instead of implementing its own request signing (unlike OAuth 1.0, which required cryptographic signatures on every request).

In production, always use HTTPS. No exceptions.

## Key Takeaways

1. **The IAM platform** (Keycloak, Okta, Auth0, etc.) is the central hub. It manages users, identity providers, and token issuance. You configure it, and it handles the complexity of OIDC and OAuth 2.0 for you.

2. **OIDC + OAuth 2.0** is the gold standard. OAuth handles authorization, OIDC adds authentication on top. The redirect-based flow keeps credentials away from your application. See my detailed guides: [OAuth](/blog/101-oauth-explained) and [OIDC](/blog/102-oidc-explained).

3. **JWTs** are the standard token format. They contain claims about the user and are cryptographically signed. The backend validates them using public keys from the JWKS endpoint, no need to call the IAM platform on every request.

4. **Asymmetric cryptography** makes the whole thing work. The IAM platform signs tokens with a private key; anyone can verify them with the public key. This is why decentralized validation is possible.

5. **Token storage** depends on the platform. For web apps, the modern recommendation is access tokens in memory and refresh tokens in `httpOnly` cookies (or the BFF pattern). For native apps, use OS-level secure storage. For Electron, use `safeStorage` or Keychain/Credential Manager.

6. **"Cookie vs Bearer Token" is a false dichotomy.** Cookies are a transport mechanism. JWTs and session IDs are token types. You can put a JWT in a cookie. Think about what type of auth you need (stateless vs stateful) and how to transport it (cookie vs header), separately.
