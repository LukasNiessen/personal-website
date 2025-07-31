---
title: "Simple Checklist: What are REST APIs"
summary: "A simple checklist for what REST APIs are"
date: "June 07 2024"
draft: false
tags:
  - REST
  - API
---

# Simple Checklist: What are REST APIs

There are thousands of articles about REST APIs already. This one simply serves as a quick checklist or reminder for designing REST APIs or similar tasks.

# 1. Paths are Resources

> Paths are resources! Not actions!

A path should always map to a resource, that is, to a _"thing"_. For example to an item, to a user, to a list of pictures and so on.

### Example

We want to define an endpoint to retrieve all items of a store. The right way to do that is this: `GET /items`. We do not define actions, so `/items/getItems` for example is wrong!

Likewise, deleting a specific item is `DELETE /items/{itemId}`. The resource here is `/items/{itemId}`. A common mistake would be to have something like `/items/delete-item/{itemId}`. This is wrong! This would not describe a resoure but an action.

# 2. Plural Paths

> Paths should use plural words!

Let's say we want to have an endpoint for retrieving a users profile picture. We should define it as something like this: `GET /users/{userId}/profile-picture`.

Of course it also makes sense if we use singular (`/user/{userId}/...`), but that is not the convention. Use plural.

# 3. HTTP Method

> The action is in the HTTP method. 

As point 1. says, a path is always a resource and not an action. The action is specified via the HTTP method. For example retrieving a profile picture would be:

`GET /users/{userId}/profile-picture`,

and deleting it would be:

`DELETE /users/{userId}/profile-picture`.

Note, the path is the same! That's because the resource is the same. And it should be this way.

Now, there is some confusion about some of the HTTP methods, especially around `POST`, `PUT`, `PATCH`, so here is a short and simple summary of the most important ones.

```
GET: Fetch resource
POST: Create new resource
PUT: Update resource
PATCH: Update resource but only partially
DELETE: Delete resource
```

# 4. HATEOAS

**⚠️ HATEOS is a core part of REST, but it's barely actually implemented in practice. So you may just skip this step if you're implementing endpoints. If you're learning however, for an interview for example, this step is important to know ⚠️**

HATEOAS = Hypermedia as the Engine of Application State

> The client navigates through the API using links provided by the server, not hardcoded URLs!

The idea is simple: instead of clients knowing all the URLs in advance, the server provides navigation links in its responses. Think of it like browsing a website - you don't memorize every URL, you follow links.

### Example

When you request an album, the response includes links to related actions:

```xml
<album>
  <name>Give Blood</name>
  <link rel="/artist" href="/artist/theBrakes" />
  <description>Awesome, short, brutish, funny and loud. Must buy!</description>
  <link rel="/instantpurchase" href="/instantPurchase/1234" />
</album>
```

The client looks for a link with `rel="/instantpurchase"` to buy the album, rather than constructing the purchase URL itself. This means:

- URLs can change without breaking clients
- New functionality can be added by including new links
- Clients are decoupled from server implementation details

So the idea is: the client can _"navigate"_ the response, just like a human navigates a website and discovers buttons and links to click.

While that's a great idea, in practice, most _"REST APIs"_ skip HATEOAS because it adds complexity and most developers build tightly-coupled client-server applications anyway.


# Tips

The following are just tips, they are not directly REST but more like often recommended practices when doing REST.

## Path Parameters vs Query Parameters

> Use path parameters for required values, query parameters for optional ones.

**Path parameters** (like `/users/{userId}`) should be used for required identifiers that are part of the resource itself.

**Query parameters** (like `/items?category=electronics&limit=10`) should be used for optional filters, pagination, sorting, and other modifiers.

## Response Status Codes

> Use proper HTTP status codes

This is just standard HTTP, not REST-specific, but important:

```
2xx: Indicates Success
4xx: Indicates Bad Request (client error)
3xx: Redirection
5xx: Indicates Internal Server Error
```

## User Authentication

> Don't put userId in request bodies

The current user's ID should typically come from the JWT token or session, not from the request body. This prevents users from impersonating others.

## Documentation

> Use Swagger/OpenAPI for documentation

Document your APIs properly. Swagger/OpenAPI is the standard tool for REST API documentation.

## Response Format

> Use JSON for response bodies

While REST doesn't require JSON, it's the de facto standard nowadays. Make your responses consistent and well-structured.

# Summary

If you implemented 1, 2 and 3, you have a very fine REST API. Strictly speaking, it's not RESTful since you need step 4 (and some other things), but most people will consider your API a very fine REST API. And as said already, barely anyone actually implements step 4.

# Notes

Please note that certain things here are simplified. For example, REST does not need to be used with HTTP at all. HTTP just happens to be the gold standard, so in 99% of all cases when we encounter REST, we encounter REST + HTTP. But as I said, this serves as a checklist, as a reminder. For detailed and _"more correct"_ infos, please consult other articles... Or, ideally, Roy Fielding's PhD thesis of course... :)

Another note, I recommended using JSON. Strictly speaking, XML should be used for REST APIs, however, the vast majority of _"REST APIs"_ nowadays use JSON.