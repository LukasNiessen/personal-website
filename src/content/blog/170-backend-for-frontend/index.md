---
title: "Backend for Frontend (BFF): What It Is and When to Use It"
summary: "A practical look at the Backend for Frontend pattern - what problem it solves, where it helps, where it does not, and a modern Next.js + FastAPI example"
date: "Apr 28 2026"
draft: false
repoUrl: ""
xLink: ""
linkedInLink: ""
tags:
  - Backend for Frontend
  - BFF
  - Architecture
  - Microservices
  - Next.js
  - FastAPI
---

# Backend for Frontend (BFF): What It Is and When to Use It

Backend for Frontend, or BFF for short, is one of those patterns that sounds fancy but is actually pretty simple once you see it in practice.

It's also one of those patterns that is easy to oversell.

A BFF is not automatically better than an API gateway, GraphQL, a normal backend, or a small aggregation service. It solves a few specific problems. It also introduces a few specific costs. So the useful question is not _"should every frontend have a BFF?"_.

The useful question is:

> Where should the logic live that turns backend/domain data into the data a specific UI needs?

Sometimes the answer is a BFF. Sometimes it is not.

Let's go through it.

## The Problem

Imagine you have a few microservices behind your system:

- `Customer` service
- `Catalog` service
- `Inventory` service
- `Wishlist` service

Now you build a mobile app and a web app on top of it.

The simple approach is to let the clients call those services directly:

```txt
                       +------------------> Customer Service
                       |
Mobile / Web ----------+------------------> Catalog Service
                       |
                       +------------------> Inventory Service
```

This can be totally fine.

If you have a small system, a small number of calls, and one frontend, direct calls may be the simplest thing. No need to introduce a pattern just because the pattern has a name.

But in bigger systems, a few problems tend to show up.

### 1. Screens Need Data From Multiple Services

Take a wishlist screen.

The screen may need:

- the user's wishlist item IDs from `Customer`
- item titles and images from `Catalog`
- stock information from `Inventory`

If the client calls everything directly, you either make many requests, or you need some fairly complex client-side orchestration.

On mobile this can hurt more because network latency is higher and less predictable. But the important point is not _"mobile is slow, therefore BFF"_.

The important point is:

> Aggregation has to live somewhere.

That somewhere could be:

- the mobile app itself
- the web app itself
- an API gateway
- a GraphQL server
- a `Wishlist` aggregation service
- a BFF

So the round-trip argument alone does **not** prove that you need a BFF. It only proves that client-side fan-out can become painful and that server-side aggregation may be useful.

Where exactly that aggregation should live depends on ownership, reuse, deployment, and how specific the aggregation is to one UI.

### 2. Services Return Domain Data, Not Screen Data

A catalog service should probably return catalog data.

It shouldn't know that the mobile wishlist row wants a tiny image, a short title, one badge, and no description. It also shouldn't know that the desktop product page wants larger images, SEO fields, related products, and more detailed pricing information.

The service owns the domain. The UI owns the presentation.

Somewhere between those two, the domain model usually has to be turned into a screen model.

For example:

```json
{
  "id": "123",
  "title": "Give Blood",
  "artist": "The Brakes",
  "imageUrl": "/images/123-small.jpg",
  "stockLabel": "Only 2 left"
}
```

This is not really a catalog object anymore. It is a wishlist-row object.

A BFF can be a good place for that. But again, not the only place. GraphQL can also solve parts of this. A shared gateway can solve parts of this. A dedicated `Wishlist` service can solve parts of this if wishlist is really a domain concept in your system.

The deciding question is: is this shape specific to one UI, or is it a reusable backend capability?

### 3. Some Client Logic Is Hard To Change Later

This is especially relevant for mobile apps.

When a web app changes, you deploy it and users usually get the new version. When a mobile app changes, you ship a new app release, users update whenever they update, and old versions can live for a long time.

So if the mobile app contains all the logic that says:

- call these three services
- join the data like this
- hide these fields
- sort the items like that
- show this label when stock is low

then changing that logic may require a mobile release.

A BFF can move some of that logic server-side. That can be useful.

But this has a limit. If the actual screen changes, or if you need new UI behavior, you still need an app release. A BFF doesn't magically make old mobile apps support new screens. It just gives you more room to change the data contract behind an existing screen.

So the realistic claim is:

> A BFF can make some UI-data changes easier to deploy, especially for clients that are hard to update.

Not:

> A BFF means you never need mobile releases anymore.

## What Is a Backend for Frontend?

A Backend for Frontend is a backend that is built for one frontend, or for one user experience.

So instead of one generic backend API for every client, you may have:

- a Web BFF
- a Mobile BFF
- maybe a Partner BFF
- maybe a TV App BFF

The frontend talks to its BFF. The BFF talks to the real backend services.

```txt
Web Client -------> Web BFF ------+
                                  |
                                  +------> Customer Service
                                  |
                                  +------> Catalog Service
                                  |
Mobile App ------> Mobile BFF ----+
                                  |
                                  +------> Inventory Service
```

The BFF does things like:

- call multiple services
- combine responses
- remove fields the UI does not need
- rename fields into UI-friendly names
- translate backend errors into UI-friendly errors
- sometimes cache or precompute data

What I would usually try to keep out of it is core business rules.

If you start implementing payment rules, inventory rules, or pricing rules in the BFF, the BFF is no longer just adapting the backend to the frontend. It is becoming a business service, and that is usually a smell.

Not always, of course. Architecture has annoying exceptions everywhere. But as a default rule:

> I would keep UI-specific orchestration in the BFF, and core domain logic deeper in the system.

## Why Not Just an API Gateway?

Sometimes an API gateway is enough.

An API gateway is usually a shared entry point in front of your backend services. It can handle things like:

- routing
- authentication
- rate limiting
- TLS termination
- logging
- request/response transformation
- sometimes aggregation

That is useful.

The difference is mostly about **purpose** and **ownership**.

An API gateway is usually general-purpose. A BFF is specific to one frontend experience.

So this is not really:

```txt
BFF good, API gateway bad
```

It is more like:

```txt
API gateway: shared edge concerns
BFF: UI-specific composition
```

They can also exist together. A request can go through an API gateway first, and then to a BFF.

```txt
Mobile App -> API Gateway -> Mobile BFF -> Services
```

The problems start when a shared gateway becomes the place for every UI-specific need.

### Example: One Endpoint Starts Serving Too Many Clients

Suppose a gateway exposes:

```txt
GET /wishlist
```

At first both web and mobile use it. Fine.

Then mobile wants a compact response because the screen only shows a small card. Web wants a larger response because it shows a full page. Later the tablet app wants something in between. Then one client wants extra recommendation data. Another wants stock warnings included. Another does not.

Now you have options:

- add `?client=mobile`
- add `?include=recommendations`
- add `/v2/wishlist`
- add `/mobile/wishlist`
- return a huge response and let each client pick what it needs

All of these can work for a while. None of them are automatically wrong.

But over time, the gateway can become a place full of UI-specific conditionals. And because it is shared, every change feels more risky than it should.

This is the situation where a BFF starts to make sense.

Not because a BFF is more "architecturally pure". But because the mobile-specific wishlist endpoint can live in the mobile-owned BFF, and the web-specific wishlist endpoint can live in the web-owned BFF.

Each team gets to change the API that exists for its own UI.

## Alternatives To a BFF

Before choosing a BFF, it is worth naming the alternatives.

### Direct Client Calls

This is the simplest option.

Use it when:

- there are only a few calls
- latency is not a problem
- the frontend is simple
- the backend API already fits the UI well enough

Direct calls are not bad. They become painful when they turn every screen into a small distributed system inside the browser or mobile app.

### API Gateway Aggregation

A gateway can expose endpoints that aggregate multiple services.

This is useful when:

- the aggregated shape is shared by many clients
- the gateway team can move fast enough
- the logic is not strongly tied to one UI

If all clients want basically the same `/wishlist` response, a gateway endpoint may be perfectly fine.

### GraphQL

GraphQL is another common answer to this problem.

It lets clients ask for the fields they need, and the GraphQL server can resolve data from many backend services.

This can be a very good fit when:

- many clients need different slices of the same graph
- you want a strongly typed schema
- you are willing to operate the GraphQL layer properly

But GraphQL is also not free. You still need to think about ownership, performance, caching, authorization, and where resolver logic belongs.

In some systems, GraphQL is basically the BFF. In others, each BFF calls GraphQL. Both can make sense.

### A Domain Aggregation Service

Sometimes the thing you are building is not actually UI-specific.

If both web and mobile need the same wishlist behavior, and later partner APIs need it too, maybe the right answer is not two BFFs. Maybe the right answer is a real `Wishlist` service.

This is an important distinction.

A BFF is good for UI-specific shaping.

A domain service is better for reusable business capability.

So if your BFF endpoint keeps growing and starts to look useful for every client, that may be a sign that the logic belongs deeper in the system.

## "But That Sounds Like More Work"

Yes. Sometimes it is.

This is the part that gets skipped too often.

A BFF is another thing to build, deploy, monitor, secure, document, and debug. Even if it is small, it still exists. It can fail. It can have bad logs. It can introduce latency. It can duplicate code from another BFF. It can become a messy mini-backend if nobody draws boundaries.

So the cost is real.

But the work also does not appear out of nowhere.

If a screen needs data from three services, someone has to compose that data:

- the client
- the gateway
- GraphQL resolvers
- a domain service
- a BFF

The BFF argument is not _"let's add work"_.

The argument is:

> If the composition is specific to one UI, maybe it should live with that UI.

That is the trade-off.

You accept some extra backend surface area in exchange for clearer ownership and a better API for that frontend.

## One Example: Next.js as a Web BFF

For web applications, one common example is Next.js.

This does not mean Next.js is required for BFFs. It also does not mean every Next.js app is automatically a good BFF. It just means that if you already have a Next.js app, Route Handlers give you a natural place to put small server-side endpoints close to the UI.

Suppose the web wishlist screen needs data from three services:

- `customer-service`
- `catalog-service`
- `inventory-service`

You could expose a route like this:

```typescript
// app/api/wishlist/route.ts
import { NextResponse } from "next/server";

export async function GET(request: Request) {
  const userId = await getUserIdFromSession(request);

  const wishlistIds = await fetch(
    `${process.env.CUSTOMER_SVC}/wishlist/${userId}`
  ).then((r) => r.json());

  const items = await Promise.all(
    wishlistIds.map(async (id: string) => {
      const [catalog, inventory] = await Promise.all([
        fetch(`${process.env.CATALOG_SVC}/items/${id}`).then((r) => r.json()),
        fetch(`${process.env.INVENTORY_SVC}/stock/${id}`).then((r) => r.json()),
      ]);

      return {
        id,
        title: catalog.title,
        artist: catalog.artist,
        imageUrl: catalog.images.small,
        price: catalog.price,
        inStock: inventory.in_stock,
        stockLabel: inventory.in_stock
          ? inventory.count <= 2
            ? `Only ${inventory.count} left`
            : "In stock"
          : "Out of stock",
      };
    })
  );

  return NextResponse.json({ items });
}
```

Then the React code calls one endpoint:

```tsx
const res = await fetch("/api/wishlist");
const { items } = await res.json();
```

The important part is not Next.js.

The important part is that the web UI now has an endpoint shaped for that web UI. The catalog service still returns catalog data. The inventory service still returns inventory data. The BFF returns wishlist-screen data.

For mobile, the BFF may be a small FastAPI or Express service instead:

```python
# mobile-bff/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/wishlist")
def get_wishlist():
    # Call customer-service, catalog-service, inventory-service
    # Return the compact shape the mobile app needs
    return {
        "items": [
            {
                "id": "123",
                "title": "Give Blood",
                "image_url": "/images/123-tiny.jpg",
                "stock_label": "Only 2 left",
            }
        ]
    }
```

Again, this is not magic.

It is just:

> Give the UI a small server-side companion when that helps.

## What About Reuse Between BFFs?

The natural worry is duplication.

Both the web BFF and mobile BFF may call the same services. They may do similar auth checks. They may translate similar errors. They may even shape similar wishlist data.

Some duplication is fine.

I am generally less worried about duplication across service boundaries than duplication inside the same codebase. The reason is that extracting shared code between services can create a different problem: now services that were supposed to move independently are coupled through a shared library.

So before extracting anything, ask:

> Does this duplication actually hurt?

If it is just a few lines of request code, maybe not.

If it is a real business rule, then yes, it probably hurts. But then the answer may not be a shared BFF library. The answer may be to move that rule into the domain service that should own it.

Old rule of thumb:

> Extract the abstraction the third time, not the second.

This still applies here.

## How Many BFFs Should You Have?

The usual answer is:

> One BFF per frontend experience.

But that is a guideline, not a law.

You may have:

- one BFF for web
- one BFF for iOS
- one BFF for Android

Or you may have:

- one BFF for web
- one shared BFF for mobile

If iOS and Android are built by the same team, offer nearly the same experience, and have similar needs, a shared mobile BFF can be totally reasonable.

If iOS and Android are owned by different teams, release differently, and keep needing different endpoint shapes, splitting them becomes more reasonable.

This is where Conway's law shows up. Systems tend to follow team structure. So a good BFF boundary is often the team boundary.

That is why I like the simple guideline:

> One experience, one BFF.

Not because it is always correct, but because it asks the right question.

## When a BFF Helps

I would consider a BFF when:

- a frontend screen needs data from multiple backend services
- different clients need meaningfully different response shapes
- mobile apps need a stable, tailored contract that can evolve server-side
- the UI team often waits for a shared gateway/backend team
- the data shaping is clearly UI-specific
- you already have a server-side place close to the UI, for example Next.js Route Handlers

The strongest case is usually a combination of these.

For example:

> Mobile and web both use the same backend services, but their screens differ, mobile is sensitive to round-trips, and the mobile team keeps needing UI-specific API changes.

That is a good BFF candidate.

## When I Would Skip It

I would skip a BFF when:

- there is only one frontend
- the frontend does not do much aggregation
- a normal backend endpoint already fits the UI
- the team cannot afford another service operationally
- the logic is really domain logic and belongs in a domain service
- GraphQL or a gateway already solves the problem well enough

Also, do not create a BFF just to proxy calls.

If the BFF endpoint is basically:

```txt
GET /api/items -> GET /catalog/items
```

and it adds no useful composition, shaping, security boundary, caching, or ownership benefit, then it may just be extra plumbing.

## Common Failure Modes

BFFs can go wrong in boring ways.

### The BFF Becomes a Mini-Monolith

This happens when every UI-specific endpoint slowly turns into business logic.

At first the BFF just maps fields. Later it calculates discounts. Then it decides whether an item can be ordered. Then it contains payment rules.

At that point, the BFF is no longer adapting the backend to the frontend. It is competing with the backend.

### Every Client Gets Its Own Copy of the Same Logic

If the web BFF, mobile BFF, and partner BFF all implement the same wishlist behavior, the behavior probably does not belong in three BFFs.

That is a sign to move the shared part into a domain service.

### The BFF Hides Bad Service Boundaries

Sometimes a BFF feels useful because the backend services are awkward.

That is okay for a while. A BFF can be a pragmatic adapter.

But if the BFF is constantly fighting the service model, maybe the backend boundaries need attention too.

### Server-Side Fan-Out Still Has a Cost

Moving 40 client requests into one BFF request improves the client experience, but the backend still does the work.

The BFF can still overload downstream services. It can still create N+1 call patterns. It still needs timeouts, retries, caching, and observability.

So server-side aggregation is not automatically cheap. It is just usually easier to control than client-side aggregation.

## Wrapping Up

Backend for Frontend is a useful pattern, but not a universal default.

The simple version is:

> A BFF is a small backend owned by a frontend team and shaped around one frontend experience.

It can help when the UI needs server-side composition, when clients need different data shapes, when mobile contracts are hard to change, or when a shared gateway is becoming full of client-specific logic.

But the alternatives are real too. Direct calls, API gateway aggregation, GraphQL, and domain aggregation services can all be the better answer depending on the system.

So I would not ask:

> Should we use a BFF?

I would ask:

> Where should this composition logic live, and who should own it?

If the honest answer is _"this logic exists only because this UI needs it"_, a BFF is worth considering.

If the honest answer is _"this is reusable backend behavior"_, it probably belongs somewhere else.
