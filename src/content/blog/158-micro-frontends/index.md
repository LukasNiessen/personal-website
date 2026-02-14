---
title: "Micro Frontends: When They Make Sense and When They Don't"
summary: "A system design look at iframes, web components, module federation, and the other ways to split a frontend — plus why you probably shouldn't."
date: "Feb 14 2026"
tags:
  - Architecture
  - System Design
  - Frontend
  - Microservices
---

# Micro Frontends: When They Make Sense and When They Don't

Microservices solved a real problem on the backend: independent deployability, team autonomy, scaling individual pieces. So naturally, people asked: can we do the same thing for the frontend? That's where micro frontends come in.

> Micro frontends = independently deliverable frontend applications composed into a greater whole.

The idea is straightforward. Instead of one big monolithic frontend that every team touches, you break it apart. Each team owns a slice of the UI end to end — frontend and backend. They build it, deploy it, ship it, without coordinating with five other teams.

Sounds great on paper. In practice, it's one of those things where the complexity cost is often higher than the problem it solves. But let's go through all the approaches first, then talk about when to actually use them.

## The Approaches

There are several ways to implement micro frontends. Each comes with its own tradeoffs. Here's a quick overview of the main ones, roughly in order of how long they've been around.

### iframes

The oldest trick in the book. An iframe embeds one HTML page inside another. Each iframe is fully isolated — its own DOM, its own CSS, its own JavaScript context. No conflicts, no style bleeding, nothing.

```html
<iframe src="https://team-checkout.example.com/cart"></iframe>
<iframe src="https://team-recommendations.example.com/widget"></iframe>
```

**The good:** Complete isolation. You literally cannot break the host page from inside an iframe. Different teams can use completely different tech stacks, different framework versions, whatever. It just works.

**The bad:** Almost everything else. iframes are terrible for responsive design. Sizing them dynamically is painful. Communication between iframes and the parent page requires `postMessage`, which is clunky. Deep linking and routing don't work naturally. Accessibility is a mess. Performance takes a hit because each iframe loads its own full page context. And they feel like iframes — users can often tell something is off.

**When it fits:** Legacy integration. You have an old system that you need to embed into a new shell, and rewriting it isn't an option. That's pretty much the only case where iframes are the right call nowadays. Some enterprise dashboards still use them for exactly this reason.

### Page-Based Decomposition

Before SPAs took over, we had the web. Multiple pages, each served from a different backend. You click a link, a new page loads. Different routes can be owned by different teams and served from different services.

```
/albums/*    → Albums service (serves full HTML pages)
/artists/*   → Artists service (serves full HTML pages)
/checkout/*  → Checkout service (serves full HTML pages)
```

A shared navigation bar stitches it all together. Each team owns its routes end to end.

**The good:** Incredibly simple. No JavaScript framework conflicts. No bundle size problems. No complex build pipelines. Standard web behavior — bookmarks, browser back/forward, deep linking, all work perfectly. Each team deploys independently by definition, since they are separate services serving separate pages.

**The bad:** Every navigation is a full page load. You lose the smooth SPA-like transitions. Shared state between pages (like a shopping cart count in the header) requires either server-side sessions or some shared storage mechanism. The user experience can feel less polished compared to a single-page app.

**When it fits:** Content-heavy sites where each section is relatively independent. Internal tools, admin panels, documentation sites. Honestly, a lot of applications that are built as SPAs would work perfectly fine as multi-page apps. We tend to over-reach for SPA frameworks.

### Web Components

The Web Component Standard lets you create custom HTML elements with encapsulated HTML, CSS, and JavaScript using the Shadow DOM. In theory, this is exactly what micro frontends need — self-contained, sandboxed UI components that don't leak styles or scripts.

```html
<checkout-cart></checkout-cart>
<recommendation-carousel></recommendation-carousel>
```

Each team publishes their micro frontend as a web component. The shell application just uses the custom HTML tags.

**The good:** Native browser standard, no framework dependency for the encapsulation layer itself. Shadow DOM gives you real CSS isolation. You can use different frameworks inside different web components. The API is just HTML elements — simple to compose.

**The bad:** The web component standard took a long time to mature. Browser support is solid now, but the ecosystem is still thinner than what you get with React or Vue. Sharing state between web components isn't standardized — you end up using custom events or a shared event bus, which gets messy at scale. Server-side rendering support is limited. And while the Shadow DOM isolates CSS, it also makes global theming harder, which is ironic since consistency is one of the things you want most in a multi-team frontend.

**When it fits:** When you need widget-level decomposition and want a standards-based approach. It works well when different teams contribute isolated, self-contained widgets to a shared page. The Financial Times, for example, uses web components to deliver reusable UI components that encapsulate their brand identity across teams.

### Module Federation (Webpack / Vite)

Module Federation was introduced in Webpack 5 (around 2020) and has since been adopted by other bundlers. The idea is that separate applications can share JavaScript modules at runtime. One app can dynamically load a component from another app — no iframe, no separate page load, just a JavaScript import that gets resolved at runtime.

```javascript
// Shell application's webpack config
new ModuleFederationPlugin({
  remotes: {
    checkout: "checkout@https://checkout.example.com/remoteEntry.js",
    recommendations: "recs@https://recs.example.com/remoteEntry.js",
  },
});
```

```jsx
// Using a remote component — looks like a normal import
const Cart = React.lazy(() => import("checkout/Cart"));
const Recs = React.lazy(() => import("recommendations/Carousel"));
```

**The good:** It feels native. Remote components behave like local ones. You can share dependencies (like React) across apps so you don't load them twice. Each team builds and deploys independently. The developer experience is relatively smooth once the setup is in place.

**The bad:** The initial setup is not trivial. Shared dependency versioning gets complicated — if team A uses React 18.2 and team B uses React 18.3, you need to figure out which one gets loaded. The runtime dependency resolution can fail in subtle ways. Debugging across remote boundaries is harder. And you're coupling yourself to a specific build tool. Also, module federation gives you no CSS isolation by default — you need to handle that separately.

**When it fits:** When you're already in a SPA world (React, Vue, Angular), you have multiple teams that need to contribute to the same application shell, and you want the end result to feel like a single app. This is currently the most popular approach for green-field micro frontend architectures in the SPA space.

### Single-SPA and Orchestration Frameworks

[single-spa](https://single-spa.js.org/) is a framework specifically built for micro frontends. It acts as a top-level router that mounts and unmounts different frontend applications based on the URL. Each sub-application can use a different framework — one can be React, another Vue, another Angular.

**The good:** Framework-agnostic by design. Handles the lifecycle (mount, unmount, update) of micro frontends for you. Has been around since 2016, so it's relatively mature.

**The bad:** It's another abstraction layer to learn and maintain. You still need to deal with shared dependencies, style isolation, and inter-app communication yourself. The complexity is real — the documentation alone should tell you something about how much there is to configure.

**When it fits:** When you genuinely have teams using different frameworks and need them to coexist in a single SPA shell. That said, if you have teams on different frameworks, I'd first ask whether the organizational structure is right.

### Server-Side Composition

Instead of composing micro frontends in the browser, you compose them on the server. Technologies like [Podium](https://podium-lib.io/) or Zalando's [Tailor](https://github.com/zalando/tailor) let you assemble fragments from different services into a single HTML response before it hits the browser.

**The good:** The browser receives a single, pre-composed page. No client-side JavaScript needed for the composition itself. Better performance for the initial load. Works well with SSR-heavy architectures.

**The bad:** You're adding server-side infrastructure for the composition layer. The communication between the composition layer and fragment services adds latency. Interactivity between fragments on the client still needs to be handled. It's more operationally complex.

**When it fits:** High-traffic e-commerce sites where initial page load performance matters a lot. Zalando and IKEA have used this approach. If your architecture is already server-rendered and performance-critical, this is worth considering.

## Quick Comparison

| Approach                | Isolation     | Setup Complexity | SPA Feel   | Performance        | Team Independence |
| ----------------------- | ------------- | ---------------- | ---------- | ------------------ | ----------------- |
| iframes                 | Full          | Low              | Poor       | Poor               | High              |
| Page-based              | Full          | Low              | None (MPA) | Good               | High              |
| Web Components          | Shadow DOM    | Medium           | Good       | Good               | Medium            |
| Module Federation       | None (manual) | High             | Native     | Good               | High              |
| Single-SPA              | None (manual) | High             | Native     | Okay               | High              |
| Server-Side Composition | Full          | High             | Depends    | Great initial load | High              |

## The Architecture Decision: Which One to Pick

Here's where it gets interesting. The question isn't really "which micro frontend technology should I use?" The question is: **do I even need micro frontends?**

### Start with the Organizational Problem

Sam Newman puts this well in his writing about microservices and user interfaces. The primary driver for micro frontends isn't technical — it's organizational. The question is about ownership.

In a traditional setup, you have a frontend team and backend teams. Adding a new feature means the frontend team makes UI changes, and one or more backend teams make API changes. Three teams, one feature. Handoffs, coordination, waiting.

```
Traditional layered model:

  [Frontend Team]     ← owns all UI
  [Backend Team A]    ← owns service A
  [Backend Team B]    ← owns service B

  New feature = 3 teams need to coordinate
```

The micro frontend model enables _stream-aligned teams_ — teams that own a vertical slice of the product, frontend through backend. This is what Matthew Skelton and Manuel Pais describe in _Team Topologies_. The team owns everything from the button the user clicks to the database row it writes.

```
Stream-aligned model:

  [Checkout Team]     ← owns checkout UI + checkout service
  [Catalog Team]      ← owns catalog UI + catalog service
  [Profile Team]      ← owns profile UI + profile service

  New feature = 1 team handles it end to end
```

That's the real benefit. Independent deployability and team autonomy. The technology choice is secondary.

### The Complexity Tax

But here's the thing. Micro frontends come with a significant complexity tax:

- **Build infrastructure.** Each micro frontend needs its own build pipeline, its own deployment, its own CI/CD. Multiply your operational overhead by the number of micro frontends.
- **Shared dependencies.** Do you share React across micro frontends or let each bundle its own? Sharing saves bytes but creates versioning headaches. Not sharing balloons your page size. There is no clean answer.
- **Consistent look and feel.** With a monolithic frontend, consistency is easy — you use the same components everywhere because it's the same codebase. With micro frontends, you need a shared design system, shared component libraries, and governance to make sure teams actually use them.
- **Cross-cutting concerns.** Authentication, routing, error handling, analytics, global state — all of these become harder when the frontend is split apart. Someone still needs to own the shell that ties everything together.
- **Testing.** Integration testing across micro frontends is significantly more complex than testing a monolithic frontend. You need contract testing, end-to-end testing across independently deployed parts, and a way to catch visual regressions.
- **Performance.** Multiple bundles, potentially duplicated dependencies, runtime composition overhead. A well-built monolithic SPA will almost always outperform a micro frontend setup in terms of raw bundle size and load time.

### When to Go Monolithic

**In my opinion:** for most teams, a monolithic frontend is the right choice. Here's why.

If you have fewer than, say, 4-5 teams working on the frontend, you probably don't have the organizational scaling problem that micro frontends solve. The coordination overhead of a monolithic frontend is manageable at that size. The complexity overhead of micro frontends is not justified.

If your teams are all using the same framework (and they should be, unless there's a very good reason not to), you're not gaining much from the isolation that micro frontends provide. A well-structured monolithic frontend with clear module boundaries, a shared component library, and good code ownership conventions (like CODEOWNERS files) gets you most of the benefits with a fraction of the complexity.

Sam Newman describes a _monolithic frontend_ pattern where the UI is a single deployable unit making calls to backend microservices. He notes this works best when a single team develops both the frontend and the supporting services. Even with multiple teams, if you can make a modular monolith work — clear boundaries, separate directories or packages per domain, good CI practices — that's preferable.

**Here's a rule of thumb I use:** if you can solve your problem with a monorepo and good module boundaries instead of micro frontends, do that.

### When Micro Frontends Make Sense

That said, there are scenarios where they genuinely help:

1. **Large organizations (5+ teams) contributing to a single frontend.** When the monolith becomes a bottleneck — merge conflicts are constant, deployments block each other, teams are stepping on each other's code — micro frontends can unlock independent delivery.

2. **Gradual migration.** You're rewriting a legacy application piece by piece. Micro frontends let you carve out sections and rebuild them with new technology while the old system still runs. The strangler fig pattern applied to the frontend.

3. **Genuinely different technology requirements.** One part of your app is a data-heavy dashboard that works best with a different rendering approach than your main consumer-facing SPA. This is rare, but it happens.

4. **Acquisition integration.** You've acquired a company and need to integrate their product into your platform. Rather than rewriting their frontend, you embed it.

### If You Do Go Micro Frontend

Here's how I'd think about picking an approach:

**You're building a content site or internal tool?** Start with page-based decomposition. It's the simplest, most robust approach. Different routes served by different teams. A shared nav ties it together. You can always add more sophistication later.

**You're embedding a legacy system?** iframes. Accept the UX limitations. Wrap it up, embed it, move on. Don't try to get clever.

**You're building a modern SPA with multiple teams?** Module Federation is the most practical choice right now. It gives you the native SPA feel with independent deployments. Pair it with a shared design system and shared dependency management.

**Performance-critical, server-rendered architecture?** Look at server-side composition. Zalando proved this works at scale.

**You want a standards-based approach and can live with some immaturity?** Web Components. The standard is solid now, but the ecosystem is still catching up.

## The Organizational Side

Whichever technical approach you pick, the organizational model matters more. A few things from Sam Newman's work on this topic that I think are important:

**Stream-aligned teams over dedicated frontend teams.** Having a separate "frontend team" creates a handoff bottleneck. Teams that own the full vertical slice — UI, API, data — deliver faster because they don't need to coordinate across team boundaries for every feature. This doesn't mean every developer needs to be full stack. It means the team as a whole has the skills to deliver end to end.

**Share specialists through enabling teams, not silos.** Good frontend developers are hard to find. The temptation is to pool them into a dedicated team. A better model: embed specialists in stream-aligned teams, or create an _enabling team_ (as Skelton and Pais describe it) whose job is to help other teams become self-sufficient. The Financial Times Origami team is a good example — they build shared web components and help other teams deliver consistent UIs without being a bottleneck.

**Consistency through shared libraries, not centralized control.** A living design system, shared UI components, and a CSS style guide can maintain consistency across teams without requiring a single team to own all the UI. It takes discipline, but it scales better than a centralized team.

**Consider a Backend for Frontend (BFF).** If your micro frontends need to aggregate data from multiple microservices, each frontend (or each client type — web, mobile, etc.) can have its own BFF. The BFF handles call aggregation and filtering, keeping the frontend code simpler. This sidesteps the problem of a central API gateway becoming a shared bottleneck. One experience, one BFF.
