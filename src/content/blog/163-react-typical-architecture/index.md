---
title: "React Project Architecture — How to Actually Structure a Frontend"
summary: "React gives you components and hooks. Everything else is your problem. Here's how to organize the rest."
date: 2026-02-24
tags:
  - Programming
  - React
  - TypeScript
  - Software Architecture
  - Frontend
  - Software Engineering
---

React is not a framework. It's a library. It gives you a component model, a handful of hooks, and a rendering engine. That's it. It has no opinion about routing, state management, data fetching, or how you organize your files. The official React docs literally say: "React doesn't have opinions on how you put files into folders."

Compare that to Angular, which prescribes modules, services, dependency injection, and a CLI that generates files in standardized locations. Or Next.js, which uses file-based routing — put a file in `app/products/page.tsx` and you have a `/products` route. The framework decides. You follow.

With plain React, you decide everything. And if you've worked on more than two React projects, you've probably noticed that every single one is structured differently. Some have a clean `features/` directory with everything nicely organized. Others have a `components/` folder with 97 files in it and no clear hierarchy. Both technically work. One will make you miserable in six months.

So let's talk about the two patterns that actually work and why.

## The Root Level

Every React project has a similar root, regardless of how you organize the code inside `src/`. Here's what a modern React + TypeScript + Vite project looks like at the top level:

```
my-app/
├── public/              # Static assets (favicon, robots.txt)
├── src/                 # All application source code
│   ├── App.tsx
│   ├── main.tsx
│   └── vite-env.d.ts
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── eslint.config.js
├── .env
├── .env.local           # git-ignored
└── .gitignore
```

Let's clarify a few things.

### Why src/?

Same reason as in any language — separation. Your source code lives in `src/`. Configuration, build output, and tooling config live at the root. Build tools target `src/` for compilation and ignore root-level configs. It's clean, it's obvious, and everyone immediately knows where the actual code lives.

### index.html

In Vite projects, `index.html` sits at the root and is the entry point. It contains a `<div id="root">` and a `<script type="module" src="/src/main.tsx">` tag. Vite serves it during development and transforms it during build. This is different from Next.js, which has no `index.html` at all — it generates HTML through its framework.

### public/

Files in `public/` are copied verbatim to the build output. No processing, no hashing, no optimization. This is for things that must keep their exact filename — favicons, `robots.txt`, `manifest.json`. Everything else (images, fonts, icons) should go into `src/assets/` so Vite can optimize them.

### Environment Variables

Vite requires all client-exposed environment variables to use the `VITE_` prefix. You access them via `import.meta.env.VITE_API_URL`. Variables without the prefix are not exposed to client code — this is a security measure, because everything in a client-side bundle is visible in the browser's DevTools.

You can type them by extending `ImportMetaEnv`:

```typescript
// vite-env.d.ts
/// <reference types="vite/client" />
interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_APP_TITLE: string
}
```

Priority order is `.env.local` > `.env.[mode]` > `.env`. Never commit `.env.local`.

## Pattern 1: Horizontal Slicing (Type-Based)

This is what you see in most tutorials and smaller projects. You group files by what they _are_ — components go with components, hooks go with hooks, services go with services.

```
src/
├── assets/
│   └── images/
│       └── logo.svg
├── components/
│   ├── ui/
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   └── index.ts
│   │   ├── Input/
│   │   │   ├── Input.tsx
│   │   │   └── index.ts
│   │   ├── Modal/
│   │   │   ├── Modal.tsx
│   │   │   └── index.ts
│   │   └── index.ts
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── Sidebar.tsx
│   │   └── RootLayout.tsx
│   ├── ProductCard.tsx
│   ├── ProductList.tsx
│   ├── CartSummary.tsx
│   ├── LoginForm.tsx
│   ├── RegisterForm.tsx
│   └── SearchBar.tsx
├── hooks/
│   ├── useAuth.ts
│   ├── useProducts.ts
│   ├── useCart.ts
│   ├── useDebounce.ts
│   └── useMediaQuery.ts
├── services/
│   ├── api-client.ts
│   ├── authService.ts
│   ├── productService.ts
│   └── cartService.ts
├── store/
│   └── useCartStore.ts
├── contexts/
│   ├── AuthContext.tsx
│   └── ThemeContext.tsx
├── pages/
│   ├── HomePage.tsx
│   ├── ProductsPage.tsx
│   ├── ProductDetailPage.tsx
│   ├── CartPage.tsx
│   ├── LoginPage.tsx
│   └── NotFoundPage.tsx
├── routes/
│   └── index.tsx
├── types/
│   ├── product.types.ts
│   ├── user.types.ts
│   ├── cart.types.ts
│   └── api.types.ts
├── utils/
│   ├── formatCurrency.ts
│   ├── formatDate.ts
│   └── cn.ts
├── styles/
│   └── globals.css
├── App.tsx
└── main.tsx
```

Here's what goes where.

**components/** holds all your React components. The `ui/` subfolder is for generic, reusable UI primitives — buttons, inputs, modals, cards. Things that have no business logic and could work in any project. Layout components (Header, Footer, Sidebar) get their own subfolder. Everything else — `ProductCard`, `LoginForm`, `CartSummary` — sits directly in `components/`.

**hooks/** contains all custom hooks. Both generic ones like `useDebounce` and `useMediaQuery`, and domain-specific ones like `useProducts` and `useAuth`.

**services/** is your API layer. A configured HTTP client (usually an Axios instance or a fetch wrapper) plus service functions that call your backend. No JSX in here — these are pure data-fetching functions.

**store/** holds your client-side global state. If you're using Zustand (which you probably should be), each store gets its own file.

**contexts/** is for React Context providers — auth state, theme, locale. Things that wrap large parts of your app and rarely change.

**pages/** contains route-level components. These are the top-level components that correspond to URLs. They compose smaller components and connect data to UI.

**types/** has shared TypeScript type definitions — API response types, domain models, enums. Types that are consumed by multiple files across the project.

**utils/** is for pure functions. Date formatting, currency formatting, classname helpers. No React, no side effects.

### When This Works

Small to medium projects. Up to maybe 20-30 components. The mental model is dead simple: "It's a hook? Goes in `hooks/`. It's a component? Goes in `components/`." Anyone new to the project can navigate it immediately.

### When This Breaks Down

The same way layered architectures always break down: as the project grows, feature-related code gets scattered everywhere. `ProductCard.tsx` lives in `components/`, `useProducts.ts` in `hooks/`, `productService.ts` in `services/`, and `product.types.ts` in `types/`. Four files in four directories for one feature. Add five more features and your `components/` folder has 40 files with no clear grouping. Adding or modifying a feature means jumping across the entire project.

## Pattern 2: Vertical Slicing (Feature-Based)

This flips the organizing principle. Instead of grouping by technical type, you group by **business feature**. Everything related to products — components, hooks, services, types — lives together under `features/products/`.

```
src/
├── assets/
│   └── images/
│       └── logo.svg
├── components/
│   └── ui/
│       ├── Button/
│       │   ├── Button.tsx
│       │   ├── Button.test.tsx
│       │   └── index.ts
│       ├── Input/
│       │   ├── Input.tsx
│       │   └── index.ts
│       ├── Modal/
│       │   ├── Modal.tsx
│       │   └── index.ts
│       └── index.ts
├── features/
│   ├── auth/
│   │   ├── components/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── LoginForm.test.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   └── PasswordReset.tsx
│   │   ├── hooks/
│   │   │   └── useAuth.ts
│   │   ├── services/
│   │   │   └── authService.ts
│   │   ├── types/
│   │   │   └── auth.types.ts
│   │   └── index.ts
│   ├── products/
│   │   ├── components/
│   │   │   ├── ProductCard.tsx
│   │   │   ├── ProductCard.test.tsx
│   │   │   ├── ProductList.tsx
│   │   │   ├── ProductFilters.tsx
│   │   │   └── ProductDetail.tsx
│   │   ├── hooks/
│   │   │   ├── useProducts.ts
│   │   │   └── useProductDetail.ts
│   │   ├── services/
│   │   │   └── productService.ts
│   │   ├── types/
│   │   │   └── product.types.ts
│   │   └── index.ts
│   ├── cart/
│   │   ├── components/
│   │   │   ├── CartSummary.tsx
│   │   │   ├── CartItem.tsx
│   │   │   └── CartDrawer.tsx
│   │   ├── store/
│   │   │   └── useCartStore.ts
│   │   ├── hooks/
│   │   │   └── useCartTotal.ts
│   │   ├── types/
│   │   │   └── cart.types.ts
│   │   └── index.ts
│   └── dashboard/
│       ├── components/
│       │   ├── DashboardStats.tsx
│       │   ├── RecentOrders.tsx
│       │   └── SalesChart.tsx
│       ├── hooks/
│       │   └── useDashboardData.ts
│       ├── services/
│       │   └── dashboardService.ts
│       └── index.ts
├── hooks/
│   ├── useDebounce.ts
│   └── useMediaQuery.ts
├── lib/
│   ├── api-client.ts
│   ├── cn.ts
│   └── formatters.ts
├── layouts/
│   ├── RootLayout.tsx
│   ├── Header.tsx
│   ├── Footer.tsx
│   └── Sidebar.tsx
├── pages/
│   ├── HomePage.tsx
│   ├── ProductsPage.tsx
│   ├── ProductDetailPage.tsx
│   ├── CartPage.tsx
│   ├── DashboardPage.tsx
│   ├── LoginPage.tsx
│   └── NotFoundPage.tsx
├── providers/
│   ├── AuthProvider.tsx
│   ├── ThemeProvider.tsx
│   └── QueryProvider.tsx
├── routes/
│   └── index.tsx
├── types/
│   ├── api.types.ts
│   └── common.types.ts
├── styles/
│   └── globals.css
├── App.tsx
└── main.tsx
```

The difference is immediately visible. When you need to work on products, everything is in `features/products/`. Components, hooks, services, types — all in one place. You don't jump across the project. When you delete a feature, you delete one folder and you're done. No orphaned files in five different directories.

### What Stays Outside features/?

Some things genuinely don't belong to any single feature.

**components/ui/** is your design system. Buttons, inputs, modals, cards — generic components with zero business logic. They could be pulled into a separate package and would still work. This aligns with the **separation of concerns** principle: UI primitives are a shared foundation, not a feature.

**hooks/** at the root level holds truly generic hooks. `useDebounce`, `useMediaQuery`, `useLocalStorage`. If it's used by three or more features, it lives here. Otherwise, keep it in the feature.

**lib/** contains shared utility code. The API client instance, helper functions, formatters. Think of it as the toolbox everyone reaches into.

**providers/** wraps your app-level context providers. Auth state, theme, TanStack Query's `QueryClientProvider`. These sit at the top of the component tree and are genuinely global.

**pages/** are the glue between routing and features. A page component composes feature components together. `ProductsPage.tsx` might render `ProductFilters` and `ProductList` from `features/products/`, plus `CartDrawer` from `features/cart/`. Pages are thin — they compose, they don't contain logic.

### The index.ts Convention

Each feature folder has an `index.ts` that re-exports its public API:

```typescript
// features/auth/index.ts
export { LoginForm } from './components/LoginForm'
export { RegisterForm } from './components/RegisterForm'
export { useAuth } from './hooks/useAuth'
export type { User, LoginCredentials } from './types/auth.types'
```

This is called a **barrel export**. It gives consumers a clean import path — `import { LoginForm } from '@/features/auth'` — and hides the internal file structure. If you refactor the internals, consumer imports don't change.

One warning though: barrel exports can hurt tree-shaking in some configurations. When a bundler encounters an import from a barrel file, it may pull in everything the barrel re-exports, even if you only use one thing. For application code this is usually fine because Vite handles it well. But be cautious with deeply nested chains of barrel files re-exporting other barrel files. Keep it to one `index.ts` per feature and you'll be fine.

### Cross-Feature Imports

When features need each other, the imports are explicit:

```typescript
// In features/cart/components/CartDrawer.tsx
import { ProductCard } from '@/features/products'
import { useAuth } from '@/features/auth'
```

Just like with the Python architecture — coupling is visible. If `cart` imports from `products`, you see it. If you ever want to extract a feature, you know exactly where the dependencies are.

## Which One Should You Pick?

Same heuristic as always.

**Start horizontal** if the project is small, if you're prototyping, or if the team is small and moves fast. Less ceremony, less structure to maintain.

**Go vertical** when the project grows, when multiple developers work on different features, or when you start losing track of which files belong to which feature. That's the signal.

**Migrate when the pain tells you to.** Most successful React projects start horizontal and evolve to vertical. You don't need to predict the future. You need to respond to the present.

## A Concrete Case: React + Vite + TanStack Query

Let's make this tangible. I'll walk through how a real feature looks using the modern React stack: TypeScript, Vite, TanStack Query for server state, Zustand for client state, and React Router for routing.

### The API Client

Every frontend needs a configured HTTP client. This lives in `lib/` because it's shared infrastructure.

```typescript
// lib/api-client.ts
import axios from 'axios'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { 'Content-Type': 'application/json' },
})

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      window.location.href = '/login'
    }
    return Promise.reject(error)
  },
)
```

One instance, configured once, used everywhere. The request interceptor attaches the auth token. The response interceptor handles global error cases like expired sessions. No component ever needs to think about this.

### Service Functions

Each feature defines its own service functions that use the shared client:

```typescript
// features/products/services/productService.ts
import { apiClient } from '@/lib/api-client'
import type { Product, CreateProductDto, ProductFilters } from '../types/product.types'

export const productService = {
  getAll: (params?: ProductFilters) =>
    apiClient.get<Product[]>('/products', { params }).then((r) => r.data),

  getById: (id: string) =>
    apiClient.get<Product>(`/products/${id}`).then((r) => r.data),

  create: (data: CreateProductDto) =>
    apiClient.post<Product>('/products', data).then((r) => r.data),

  update: (id: string, data: Partial<CreateProductDto>) =>
    apiClient.patch<Product>(`/products/${id}`, data).then((r) => r.data),

  delete: (id: string) =>
    apiClient.delete(`/products/${id}`),
}
```

These are plain async functions. No React, no hooks, no state. Just data fetching. This separation matters — you can call these from hooks, from tests, from scripts, from anywhere.

### TanStack Query Hooks

This is where TanStack Query changes everything. Before it, you'd call service functions in `useEffect`, store results in `useState`, track loading and error states manually, and implement caching yourself. TanStack Query eliminates all of that.

```typescript
// features/products/hooks/useProducts.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { productService } from '../services/productService'
import type { ProductFilters, CreateProductDto } from '../types/product.types'

export const productKeys = {
  all: ['products'] as const,
  lists: () => [...productKeys.all, 'list'] as const,
  list: (filters: ProductFilters) => [...productKeys.lists(), filters] as const,
  details: () => [...productKeys.all, 'detail'] as const,
  detail: (id: string) => [...productKeys.details(), id] as const,
}

export function useProducts(filters: ProductFilters) {
  return useQuery({
    queryKey: productKeys.list(filters),
    queryFn: () => productService.getAll(filters),
  })
}

export function useProduct(id: string) {
  return useQuery({
    queryKey: productKeys.detail(id),
    queryFn: () => productService.getById(id),
    enabled: !!id,
  })
}

export function useCreateProduct() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateProductDto) => productService.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: productKeys.lists() })
    },
  })
}
```

A few things worth unpacking.

The `productKeys` object is a **query key factory**. It organizes cache keys hierarchically, which makes invalidation precise. When you create a product, you invalidate all list queries (`productKeys.lists()`) but leave detail queries untouched. Without this pattern, you end up with `queryKey: ['products']` everywhere and invalidating too much or too little.

`useProducts` returns `{ data, isLoading, isError, error }` — all the state you need. No `useState`, no `useEffect`, no loading boolean you forgot to set back to false. TanStack Query handles caching, background refetching, stale-while-revalidate, and request deduplication out of the box.

`useCreateProduct` uses `useMutation` and invalidates the product list cache on success. The next time a component that uses `useProducts` renders, it'll automatically refetch fresh data.

### Client State with Zustand

Not everything comes from the server. Some state is purely client-side — a shopping cart, a sidebar toggle, a draft form. That's where Zustand comes in.

```typescript
// features/cart/store/useCartStore.ts
import { create } from 'zustand'
import type { CartItem } from '../types/cart.types'

interface CartStore {
  items: CartItem[]
  addItem: (item: CartItem) => void
  removeItem: (id: string) => void
  clear: () => void
}

export const useCartStore = create<CartStore>((set) => ({
  items: [],
  addItem: (item) =>
    set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) =>
    set((state) => ({ items: state.items.filter((i) => i.id !== id) })),
  clear: () => set({ items: [] }),
}))
```

No providers, no boilerplate, no wrapping your app in context. Import the store, use it. Zustand only re-renders components that subscribe to the specific state they read, so performance is good by default.

The reason I recommend Zustand over Redux or Context for global client state: it's simpler (drastically less boilerplate), faster (fine-grained selectors prevent unnecessary re-renders), and doesn't require wrapping your component tree in providers.

### Routing

Route definitions live in `routes/`. With React Router v6+, you typically define routes as a configuration object:

```typescript
// routes/index.tsx
import { createBrowserRouter } from 'react-router-dom'
import { lazy, Suspense } from 'react'
import { RootLayout } from '@/layouts/RootLayout'
import { NotFoundPage } from '@/pages/NotFoundPage'

const HomePage = lazy(() => import('@/pages/HomePage'))
const ProductsPage = lazy(() => import('@/pages/ProductsPage'))
const ProductDetailPage = lazy(() => import('@/pages/ProductDetailPage'))
const DashboardPage = lazy(() => import('@/pages/DashboardPage'))
const LoginPage = lazy(() => import('@/pages/LoginPage'))

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <NotFoundPage />,
    children: [
      { index: true, element: <Suspense><HomePage /></Suspense> },
      { path: 'products', element: <Suspense><ProductsPage /></Suspense> },
      { path: 'products/:id', element: <Suspense><ProductDetailPage /></Suspense> },
      { path: 'dashboard', element: <Suspense><DashboardPage /></Suspense> },
      { path: 'login', element: <Suspense><LoginPage /></Suspense> },
    ],
  },
])
```

`lazy()` combined with `Suspense` gives you **route-based code splitting** for free. Each page is loaded only when the user navigates to it. Vite automatically creates separate chunks at `import()` boundaries. This is the single highest-impact performance optimization you can do in a React SPA, and it takes almost no effort.

### How a Page Composes Features

Pages are thin. They pull together components from multiple features:

```typescript
// pages/ProductsPage.tsx
import { ProductList } from '@/features/products'
import { CartDrawer } from '@/features/cart'
import { useProducts } from '@/features/products'

export default function ProductsPage() {
  const { data: products, isLoading } = useProducts({})

  if (isLoading) return <ProductsPageSkeleton />

  return (
    <div>
      <h1>Products</h1>
      <ProductList products={products ?? []} />
      <CartDrawer />
    </div>
  )
}
```

That's it. The page knows _what_ to show but not _how_ things work internally. `ProductList` handles rendering products. `CartDrawer` manages its own state via Zustand. `useProducts` handles data fetching, caching, and loading states. The page just composes them.

## Best Practices

A few things that matter regardless of which architecture you pick.

### Co-locate Everything

Tests, styles, types — put them next to the component they belong to.

```
Button/
├── Button.tsx
├── Button.test.tsx
├── Button.module.css
└── index.ts
```

When you delete a component, everything related goes with it. No orphaned test files in a `__tests__/` directory three levels up that nobody remembers to clean up. This is Kent C. Dodds' **co-location principle**: place code as close to where it's relevant as possible.

The exception is end-to-end tests. Those span the entire application and belong at the project root in an `e2e/` folder.

### Use Absolute Imports

Never write `../../../components/ui/Button`. Configure path aliases instead.

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

```typescript
// vite.config.ts
import path from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

Now you write `import { Button } from '@/components/ui'`. It's cleaner, it's refactoring-friendly, and you never have to count dots.

Alternatively, the `vite-tsconfig-paths` plugin reads your `tsconfig.json` paths and applies them to Vite automatically — one config, one source of truth.

### Use Error Boundaries

React doesn't provide a function component error boundary, so you need either a class component or the `react-error-boundary` library. Wrap lazy-loaded routes and major feature sections with them.

```typescript
import { ErrorBoundary } from 'react-error-boundary'

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <p>Something went wrong.</p>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  )
}

// Wrap feature sections
<ErrorBoundary FallbackComponent={ErrorFallback}>
  <Suspense fallback={<Loading />}>
    <LazyRoute />
  </Suspense>
</ErrorBoundary>
```

Without error boundaries, a single component crash takes down your entire app. With them, the crash is isolated to the boundary, and the user can retry or navigate elsewhere.

### Separate Server State from Client State

This might be the most impactful architectural decision you make. Server state (data from your API) and client state (UI toggles, form drafts, cart contents) are fundamentally different things. They have different lifecycles, different caching needs, and different update patterns.

Use **TanStack Query** for server state. Use **Zustand** (or just `useState`) for client state. Don't shove everything into one global store. The days of putting your entire API response into Redux are over.

## Wrapping Up

React gives you freedom and expects you to make good choices with it. The two patterns here — horizontal slicing for smaller projects, vertical slicing for larger ones — cover most real-world codebases.

The key insight is that these aren't permanent decisions. Start simple. Add structure when the lack of it starts hurting. Move feature-related code together when you notice you're constantly jumping between five directories to change one thing. The best architecture isn't the most sophisticated one — it's the one your team can navigate without thinking.
