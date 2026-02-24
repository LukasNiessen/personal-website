---
title: "Python Project Architecture — The Two Most Common Patterns"
summary: "Python doesn't tell you how to structure your project. Here's how most teams actually do it, and why."
date: 2026-02-24
tags:
  - python
  - fastapi
  - architecture
  - software-engineering
  - best-practices
---

Python doesn't care how you organize your code. And that's both a blessing and a curse.

If you come from something like Django, Rails, or Next.js, you're used to a framework telling you where things go. Next.js uses file-based routing, so the folder structure _is_ the configuration. Rails decides for you — models go here, controllers go there, migrations live in that folder. You don't think about it. You just follow the convention.

Python itself has none of that. It gives you modules, packages, and an import system. That's it. The rest is on you.

This means every Python team ends up making their own architectural decisions. And if you've worked on more than one Python project, you've probably noticed that no two look the same. Some are clean and well-structured. Others are a disaster where everything lives in one flat directory and you have no idea what depends on what.

So how do you actually structure a Python project? There are two dominant patterns. Let's go through both.

## The Root Level

Before we get into the two patterns, let's talk about what the root of every Python project looks like. Because this part is the same regardless of which architecture you pick.

```
my-project/
├── pyproject.toml
├── .env
├── .gitignore
├── README.md
├── src/
│   └── myapp/
│       └── ...
├── tests/
│   └── ...
└── alembic/            # if you use DB migrations
```

A few things are worth explaining here.

### pyproject.toml

This is the **single configuration file** for your Python project. It was introduced through PEP 518 and PEP 621 to replace the old `setup.py`, `setup.cfg`, `requirements.txt`, `.flake8`, `mypy.ini`, and `pytest.ini` mess. Instead of having six different config files scattered around your root, you get one.

It has three main sections. `[build-system]` tells tools how to build your package. `[project]` holds metadata like the name, version, and dependencies. And `[tool.*]` sections configure your tooling — pytest, ruff, mypy, whatever you use.

```toml
[project]
name = "my-app"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.100",
    "pydantic>=2.0",
    "sqlalchemy>=2.0",
]

[tool.pytest.ini_options]
addopts = ["--import-mode=importlib"]
testpaths = ["tests"]

[tool.ruff]
line-length = 88
```

The key insight: `pyproject.toml` is **declarative and statically parseable**. Tools can read your project metadata without executing any Python code. That's a big deal compared to the old `setup.py`, which was executable Python — meaning you had to _run_ it just to read metadata.

### Why the src/ Folder?

This one trips people up. Why not just put your package directly in the root?

```
# flat layout (no src/)
my-project/
├── pyproject.toml
├── myapp/
│   └── __init__.py
└── tests/

# src layout
my-project/
├── pyproject.toml
├── src/
│   └── myapp/
│       └── __init__.py
└── tests/
```

The reason is Python's import system. When you run `python` from your project root, the current directory is automatically added to `sys.path`. With a flat layout, `import myapp` imports from the local directory — not from the installed version. This can mask packaging bugs. You might forget to include a file in your distribution, and your tests still pass because they're importing the local copy.

With the `src/` layout, `myapp` lives inside `src/`, which is _not_ on `sys.path`. You're forced to install the package (`pip install -e .`) before you can import it. This means your tests always validate the installed version, which is exactly what your users will get.

The Python Packaging Authority (PyPA) and pytest both recommend this approach. It's a small upfront cost for a real safety net.

This adheres to the principle of **separation of concerns**: your importable code lives in `src/`, your tests live in `tests/`, your config lives at the root. Everything has a clear home.

## Pattern 1: Horizontal Slicing (Layered Architecture)

This is the most common pattern you'll see, especially in smaller to mid-sized projects. The idea is simple: you organize code by **technical responsibility**. Each folder represents a layer.

```
my-project/
├── pyproject.toml
├── .env
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── main.py
│       │
│       ├── routes/              # HTTP layer
│       │   ├── __init__.py
│       │   ├── users.py
│       │   └── orders.py
│       │
│       ├── services/            # Business logic
│       │   ├── __init__.py
│       │   ├── user_service.py
│       │   └── order_service.py
│       │
│       ├── models/              # Database models (SQLAlchemy, etc.)
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── order.py
│       │
│       ├── schemas/             # Pydantic models
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── order.py
│       │
│       ├── repositories/        # Data access
│       │   ├── __init__.py
│       │   ├── user_repo.py
│       │   └── order_repo.py
│       │
│       └── core/                # Config, DB connection, shared stuff
│           ├── __init__.py
│           ├── config.py
│           └── database.py
│
└── tests/
    ├── test_routes/
    ├── test_services/
    └── test_models/
```

Let's break down why each layer exists.

**Routes** (sometimes called `routers/` or `api/`) handle the HTTP layer. This is where your endpoint definitions live. A route parses the incoming request, calls the appropriate service, and returns a response. The key rule: **routes should contain minimal logic**. If you find yourself writing business rules in a route handler, something is wrong. This is the **Single Responsibility Principle** in action — routes are responsible for HTTP concerns, nothing else.

**Services** contain your business logic. This is where the actual work happens. A service orchestrates operations, enforces rules, and coordinates between repositories. For example, when a user places an order, the `order_service` might check inventory, calculate pricing, create the order record, and trigger a notification — all in one method.

**Models** define your database tables. If you're using SQLAlchemy, this is where your ORM models live. They describe the structure of your data and the relationships between tables. Models should be data-centric. They shouldn't contain business logic.

**Schemas** are your Pydantic models. They handle request validation, response serialization, and data transfer between layers. Keeping them separate from your database models is important — your API contract and your database schema are two different things. They evolve independently, and coupling them is a fast track to pain.

**Repositories** abstract away your data access. All database queries live here. This keeps SQL out of your services and makes it trivial to swap a database implementation for an in-memory test double. This is a direct application of the **Dependency Inversion Principle**: your services depend on a `UserRepository` abstraction, not on the concrete SQLAlchemy implementation.

**Core** holds cross-cutting concerns. Configuration, database connections, middleware, exception handlers. Things that don't belong to any single layer but are used by all of them.

### When This Works

This pattern is great for smaller projects, microservices, and teams that are used to MVC-style patterns. The mental model is straightforward: "Where does HTTP stuff go? Routes. Where does business logic go? Services." Easy to explain, easy to follow.

### When This Breaks Down

As the project grows, you start feeling the pain. Adding a new feature — say, notifications — means touching files across _every_ directory. You create `routes/notifications.py`, `services/notification_service.py`, `models/notification.py`, `schemas/notification.py`, and `repositories/notification_repo.py`. Five files in five different folders for a single feature. The changes are scattered, and reviewing a pull request becomes an exercise in jumping between directories.

This is a well-known problem with layered architectures. The technical layers group things that change together for different reasons, while features group things that change together for the same reason.

## Pattern 2: Vertical Slicing (Feature-Based Architecture)

This is the alternative. Instead of organizing by technical layer, you organize by **business domain**. Each feature gets its own directory, and that directory contains everything the feature needs.

```
my-project/
├── pyproject.toml
├── .env
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── main.py
│       │
│       ├── auth/                 # Everything for authentication
│       │   ├── __init__.py
│       │   ├── router.py
│       │   ├── service.py
│       │   ├── models.py
│       │   ├── schemas.py
│       │   ├── dependencies.py
│       │   ├── exceptions.py
│       │   └── constants.py
│       │
│       ├── users/                # Everything for user management
│       │   ├── __init__.py
│       │   ├── router.py
│       │   ├── service.py
│       │   ├── models.py
│       │   ├── schemas.py
│       │   └── exceptions.py
│       │
│       ├── orders/               # Everything for orders
│       │   ├── __init__.py
│       │   ├── router.py
│       │   ├── service.py
│       │   ├── models.py
│       │   ├── schemas.py
│       │   └── exceptions.py
│       │
│       ├── core/                 # Shared infrastructure
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── database.py
│       │   ├── exceptions.py    # Base exception classes
│       │   └── models.py        # Base model classes
│       │
│       └── common/               # Shared utilities
│           ├── __init__.py
│           ├── pagination.py
│           └── security.py
│
└── tests/
    ├── auth/
    ├── users/
    └── orders/
```

Notice the difference. When you work on the `orders` feature, everything you need is in one folder. Router, service, models, schemas — all in `orders/`. You don't jump between five directories.

This aligns with **domain-driven design** thinking. Each feature folder maps to a bounded context. The `auth/` module changes only when authentication requirements change. The `orders/` module changes only when order logic changes. That's the **Single Responsibility Principle** applied at the module level.

### What Stays Shared?

Two folders typically remain outside the feature structure.

**Core** contains genuinely global infrastructure: database connections, configuration, base model classes, middleware. Things that cut across all features. If it's used by every feature, it belongs in `core/`.

**Common** (or `utils/`) holds shared utilities like pagination helpers, authentication decorators, or date formatting functions. The rule of thumb: if something is used by three or more features, move it to `common/`. Otherwise, keep it inside the feature.

### Cross-Feature Dependencies

When features need to talk to each other, the imports are explicit.

```python
# In orders/service.py
from myapp.users.service import get_user_by_id
from myapp.auth.dependencies import require_auth
```

This makes coupling visible. If `orders` imports from `users`, you can see it right there in the imports. No hidden dependencies, no surprises. If you ever want to extract a feature into its own service, you know exactly what the dependency graph looks like.

### When This Works

Larger applications. Monoliths with multiple bounded contexts. Teams where different developers work on different features in parallel. Each feature is self-contained, so a developer working on `orders` rarely needs to look at `auth` files. It scales better as the project grows.

### When This Breaks Down

For very small projects, this is overkill. If your app has two or three endpoints, the overhead of per-feature directories isn't worth it. You're creating folders and files that add structure without adding clarity. In that case, start with the horizontal approach and migrate to vertical when you feel the pain.

## Which One Should You Pick?

There's no universal answer. But here's a reasonable heuristic.

**Start horizontal** if your project is small, if you're building a microservice with a single bounded context, or if your team is more comfortable with the MVC mental model. It's simpler to set up and easier to understand at a glance.

**Go vertical** if you're building something larger, if you anticipate multiple developers working on different features, or if you're thinking in terms of business domains rather than technical layers.

**Switch when the pain tells you to.** Many projects start horizontal and migrate to vertical as they grow. That's completely fine. Architecture is not a one-time decision. It's something you revisit as the project evolves.

## A Concrete Case: FastAPI Backend

Everything above was fairly abstract. Let's make it concrete. FastAPI is probably the most popular choice for Python backends right now, and it's a perfect example of Python's "figure it out yourself" philosophy. FastAPI gives you a powerful framework — automatic validation, dependency injection, async support, auto-generated docs — but it says nothing about how to organize your files.

So let's build one. I'll use the vertical slicing pattern since that's what scales better for real projects, and I'll walk through each piece.

### The Full Structure

```
my-project/
├── pyproject.toml
├── alembic.ini
├── .env
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── main.py                  # App creation, wiring
│       │
│       ├── core/                    # Shared infrastructure
│       │   ├── __init__.py
│       │   ├── config.py            # Pydantic Settings
│       │   ├── database.py          # Engine, session, get_db
│       │   └── exceptions.py        # Base exception classes + handlers
│       │
│       ├── auth/
│       │   ├── __init__.py
│       │   ├── router.py
│       │   ├── schemas.py
│       │   ├── service.py
│       │   ├── dependencies.py      # get_current_user
│       │   └── utils.py             # JWT, password hashing
│       │
│       ├── users/
│       │   ├── __init__.py
│       │   ├── router.py
│       │   ├── schemas.py
│       │   ├── service.py
│       │   ├── repository.py
│       │   ├── models.py
│       │   └── dependencies.py
│       │
│       └── products/
│           ├── __init__.py
│           ├── router.py
│           ├── schemas.py
│           ├── service.py
│           ├── repository.py
│           ├── models.py
│           └── dependencies.py
│
└── tests/
    ├── conftest.py
    ├── auth/
    ├── users/
    └── products/
```

Let's walk through how the pieces fit together.

### main.py — Where Everything Connects

The `main.py` file is the entry point. It creates the FastAPI app, wires up middleware, registers exception handlers, and mounts the routers. It shouldn't contain business logic. Think of it as the wiring diagram.

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from myapp.core.config import settings
from myapp.core.database import engine
from myapp.core.exceptions import register_exception_handlers
from myapp.auth.router import router as auth_router
from myapp.users.router import router as users_router
from myapp.products.router import router as products_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: warm caches, check DB, etc.
    yield
    # shutdown: release resources
    await engine.dispose()


app = FastAPI(title="My API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(products_router, prefix="/api/products", tags=["products"])
```

A few things to note here. The `lifespan` context manager replaces the old `@app.on_event("startup")` and `@app.on_event("shutdown")` decorators, which are deprecated. Code before `yield` runs once when the app starts. Code after `yield` runs once when it shuts down.

Each feature exposes a single `router` that gets mounted with a prefix. So `@router.get("/me")` inside `users/router.py` becomes `GET /api/users/me`. The feature doesn't know or care about its prefix — `main.py` decides that.

### The Database Layer

This is the foundation everything else builds on.

```python
# core/database.py
from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from myapp.core.config import settings

engine = create_async_engine(settings.database_url, pool_size=5, max_overflow=10)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


DbSession = Annotated[AsyncSession, Depends(get_db)]
```

The `get_db` function is a **dependency with yield**. Code before `yield` sets things up, `yield` hands the session to whoever requested it, and code after `yield` handles cleanup. If everything went fine, we commit. If something threw an exception, we rollback. FastAPI runs this automatically for every request.

`expire_on_commit=False` is important for async SQLAlchemy. Without it, accessing an attribute after commit would trigger a lazy load — which is a synchronous database call and would blow up in an async context.

That last line — `DbSession = Annotated[AsyncSession, Depends(get_db)]` — is an **annotated type alias**. This is the modern way to declare dependencies in FastAPI. Instead of writing `db: AsyncSession = Depends(get_db)` in every endpoint, you write `db: DbSession`. Define it once, import it everywhere.

### How a Feature Looks Inside

Let's look at a complete feature. Here's `products/`.

**Schemas** define the API contract:

```python
# products/schemas.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    price: float = Field(..., gt=0)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    price: float | None = Field(default=None, gt=0)


class ProductRead(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    created_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

`ProductCreate` is what the client sends when creating a product. `ProductUpdate` is for partial updates — all fields are optional, so the client sends only what changed. `ProductRead` is what the API returns. `from_attributes=True` lets Pydantic read directly from SQLAlchemy model attributes, so you can return ORM objects and FastAPI serializes them automatically.

Note that `ProductCreate` and `ProductRead` are different types on purpose. Your API contract and your database schema are two different things. They evolve independently.

**Repository** handles all database access:

```python
# products/repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from myapp.products.models import Product
from myapp.products.schemas import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, product_id: int) -> Product | None:
        result = await self.db.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_many(self, skip: int = 0, limit: int = 20) -> list[Product]:
        result = await self.db.execute(
            select(Product).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, data: ProductCreate, created_by: int) -> Product:
        product = Product(**data.model_dump(), created_by=created_by)
        self.db.add(product)
        await self.db.flush()
        await self.db.refresh(product)
        return product

    async def update(self, product: Product, data: ProductUpdate) -> Product:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        await self.db.flush()
        await self.db.refresh(product)
        return product
```

All SQL lives here. The service layer never touches the database directly. This is the **Dependency Inversion Principle** — the service depends on an abstraction (the repository), not on SQLAlchemy directly. If you ever swap databases or need a test double, you only change the repository.

Note `model_dump(exclude_unset=True)` on the update. This gives you only the fields the client actually sent, which makes PATCH semantics work correctly. If the client sends `{"price": 29.99}`, only the price gets updated. Everything else stays untouched.

**Service** contains business logic:

```python
# products/service.py
from myapp.core.exceptions import NotFoundError
from myapp.products.repository import ProductRepository
from myapp.products.schemas import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def get_by_id(self, product_id: int):
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise NotFoundError("Product", product_id)
        return product

    async def create(self, data: ProductCreate, created_by: int):
        return await self.repository.create(data, created_by=created_by)

    async def update(self, product_id: int, data: ProductUpdate):
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise NotFoundError("Product", product_id)
        return await self.repository.update(product, data)
```

The service raises domain exceptions like `NotFoundError`, not HTTP exceptions. It has no idea it's running inside a web framework. This is important — your business logic should be framework-agnostic. The mapping from domain exceptions to HTTP responses happens in the exception handlers that we registered in `main.py`.

**Dependencies** wire everything together:

```python
# products/dependencies.py
from typing import Annotated
from fastapi import Depends

from myapp.core.database import DbSession
from myapp.products.repository import ProductRepository
from myapp.products.service import ProductService


def get_product_repository(db: DbSession) -> ProductRepository:
    return ProductRepository(db)


def get_product_service(
    repo: Annotated[ProductRepository, Depends(get_product_repository)],
) -> ProductService:
    return ProductService(repo)
```

This is FastAPI's dependency injection in action. When an endpoint asks for a `ProductService`, FastAPI sees that it needs a `ProductRepository`, which needs a `DbSession`, which needs `get_db`. It resolves the entire chain automatically. And because of **request-scoped caching**, if multiple dependencies in the same request all need `get_db`, they get the exact same session. That's how you get transactional consistency within a single request without passing the session around manually.

**Router** ties it all together for HTTP:

```python
# products/router.py
from typing import Annotated
from fastapi import APIRouter, Depends, Query, status

from myapp.auth.dependencies import get_current_user
from myapp.products.dependencies import get_product_service
from myapp.products.schemas import ProductCreate, ProductRead, ProductUpdate
from myapp.products.service import ProductService
from myapp.users.schemas import UserRead

router = APIRouter()

ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
CurrentUser = Annotated[UserRead, Depends(get_current_user)]


@router.get("/", response_model=list[ProductRead])
async def list_products(
    product_service: ProductServiceDep,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
):
    return await product_service.list(skip=skip, limit=limit)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    product_service: ProductServiceDep,
    current_user: CurrentUser,
):
    return await product_service.create(data, created_by=current_user.id)


@router.patch("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    product_service: ProductServiceDep,
    current_user: CurrentUser,
):
    return await product_service.update(product_id, data)
```

The router is thin. It declares the HTTP interface — method, path, request/response types — and delegates to the service. No business logic here. FastAPI handles all the heavy lifting: it parses the request body into your Pydantic schema, validates it, returns 422 with detailed errors if validation fails, and serializes the response through the `response_model`.

### Async vs. Sync — A Quick Note

FastAPI supports both `async def` and plain `def` for endpoint functions, and the distinction matters.

Use `async def` when you're calling async libraries — things like `asyncpg`, `httpx`, `aiofiles`. These return awaitables, and you need `await`.

Use plain `def` when you're calling synchronous/blocking libraries — like `requests`, synchronous database drivers, or heavy CPU work. FastAPI automatically runs `def` endpoints in a thread pool, so they don't block the event loop.

The trap: if you write `async def` but then call blocking code inside it, you block the entire event loop. Every other concurrent request stalls until your blocking call finishes. If you're unsure, use `def` — it's the safer default.

### Config with Pydantic Settings

```python
# core/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    cors_origins: list[str] = ["http://localhost:3000"]
    secret_key: str
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
```

The `@lru_cache` decorator ensures the `.env` file is read exactly once. Every subsequent call returns the cached `Settings` instance. Environment variables take priority over `.env` values, so the same code works in development (where you have a `.env` file) and production (where you set env vars through your deployment platform).

## Best Practices (Regardless of Pattern)

A few things that apply no matter which structure you pick.

### Test Everything

If you don't have tests, your codebase is not evolvable. You change one thing, and something else breaks three layers away. Without tests, you don't know about it until a user reports it.

```
tests/
├── conftest.py              # Shared fixtures
├── unit/
│   ├── test_user_service.py
│   └── test_order_service.py
├── integration/
│   ├── test_user_api.py
│   └── test_database.py
└── e2e/
    └── test_full_flow.py
```

Separate unit tests, integration tests, and end-to-end tests. Unit tests are fast and test a single function or class in isolation. Integration tests verify that components work together (e.g., your service actually talks to the database correctly). E2E tests validate the full flow from request to response.

Use `conftest.py` for shared fixtures. Keep your test structure roughly mirroring your source structure. And configure pytest properly in your `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = ["--import-mode=importlib"]
testpaths = ["tests"]
```

### Put Config Where Config Belongs

Configuration lives in `.env` files for local development and in environment variables for production. It does _not_ live hardcoded in your application code. When you need a database URL, an API key, or a feature flag — read it from config, not from a string literal in `service.py`.

This is the **separation of concerns** again. Your code describes _what_ to do. Your config describes _how_ to connect to the outside world. Mixing them makes your application rigid and painful to deploy.

### Keep __init__.py Files Lean

Every Python package directory needs an `__init__.py` file (or at least, it's strongly recommended). But keep them empty or close to empty. At most, use them to define the public API of a package:

```python
# users/__init__.py
from .service import UserService
from .schemas import UserCreate, UserResponse
```

Don't put logic in there. Don't put database connections in there. It runs on every import, so anything expensive will slow your entire application down.

## Wrapping Up

Python's lack of opinion about project structure can feel overwhelming, especially when you're starting out. But it's also the reason Python is so versatile — the same language works for web apps, data pipelines, CLI tools, and machine learning.

The two patterns I've laid out here — horizontal and vertical slicing — cover the vast majority of real-world Python projects. Pick one, be consistent, and adapt when the project tells you to. Architecture isn't about getting it right from the start. It's about making decisions you can evolve later.
