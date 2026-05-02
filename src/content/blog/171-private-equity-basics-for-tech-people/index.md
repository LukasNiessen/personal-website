---
title: "Private Equity Basics for Tech People"
summary: "A practical crash course on private equity: how funds work, how deals work, the words people use, what matters when building PE software, and where AI actually changes the workflow."
date: "Apr 29 2024"
tags:
  - Private Equity
  - Finance
  - Product
  - AI
  - FinTech
---

# Private Equity Basics for Tech People

Private equity is one of those fields that sounds more mysterious than it actually is.

Not because it is simple. It is not. The legal structures, tax details, financing terms, incentives, fund accounting, and negotiations can get very complex very quickly.

But the basic idea is simple:

> A private equity firm raises money, buys companies, tries to make them more valuable, and sells them later.

That's the core.

## What Is Private Equity?

Private equity, or PE, means investing in companies that are not publicly traded, or taking public companies private.

The most common mental model is this:

- Public market investor: buys shares of Microsoft, Apple, or Siemens on an exchange
- Private equity fund: buys a private company, or buys enough of a company to control it

That control part matters.

Private equity is usually not just "we bought some shares and hope the price goes up." In buyout private equity, the firm often takes control, sits on the board, changes management incentives, improves operations, changes pricing, buys competitors, sells business units, refinances debt, and eventually exits.

The [SEC investor guide on private equity funds](https://www.investor.gov/introduction-investing/investing-basics/investment-products/private-investment-funds/private-equity) describes the typical strategy in the same direction: PE funds often focus on long-term investments, take controlling interests, and actively engage with portfolio companies to increase value.

So compared to public investing, PE is:

- less liquid
- more operational
- more private
- more document-heavy
- more relationship-driven
- often more leveraged
- measured over years, not days

One important note: venture capital is technically a form of private equity. But in normal business conversations, when people say "private equity", they usually mean buyout funds or growth equity, not seed-stage VC.

## The Basic Structure

The easiest way to understand PE is to separate the people who provide the money from the people who manage the money.

```txt
Pension funds, endowments, insurers, family offices
             |
             | commit capital
             v
        Private Equity Fund
             ^
             | managed by
             |
      GP / PE Firm / Adviser
             |
             | buys and manages
             v
      Portfolio Companies
```

There are two key roles:

**LPs** are limited partners. They provide most of the capital. Think pension funds, university endowments, insurance companies, sovereign wealth funds, family offices, and sometimes wealthy individuals.

**GPs** are general partners. They manage the fund, source deals, make investment decisions, support portfolio companies, and decide when to sell.

In reality, there are multiple legal entities: fund, general partner, management company, adviser, carry vehicle, co-invest vehicles, SPVs. For now, don't worry about all of them. But if you're building PE software, you very much need to care later, because legal entity modeling becomes a real domain problem.

The [SEC guide on starting a private fund](https://www.sec.gov/resources-small-businesses/capital-raising-building-blocks/starting-private-fund) is a useful reference here. It describes private funds as vehicles that pool money from multiple investors, often using capital commitments that are called down over time.

## Commitments and Capital Calls

This part is unintuitive if you are used to normal investing.

LPs usually do not wire all the money on day one.

Instead, they commit an amount.

Example:

```txt
LP A commits: 100m
LP B commits: 200m
LP C commits: 700m

Total fund size: 1bn
```

The GP does not immediately have 1bn sitting in a bank account. The GP has the legal right to call that money when needed.

When the GP finds an investment, it sends a **capital call**:

```txt
We need 10% of your commitment by May 15.

LP A wires: 10m
LP B wires: 20m
LP C wires: 70m
```

This is also called a drawdown.

For software this matters a lot. A PE system should not only store "investor invested 100m". It needs to distinguish:

- committed capital
- called capital
- contributed capital
- unfunded commitment
- distributions
- recallable distributions

These are not small differences. They drive fund accounting, reporting, LP statements, and performance metrics.

## Fund Life Cycle

A PE fund usually has a finite life, often around 10 years, sometimes with extensions.

The rough flow looks like this:

```txt
Fundraising
    |
    v
Investment period
    |
    | source deals, buy companies, make add-on acquisitions
    v
Holding period / value creation
    |
    | improve operations, grow revenue, pay down debt
    v
Exit period
    |
    | sell companies, return money
    v
Distributions to LPs and GP
```

The first years are usually about deploying capital. Later years are more about managing and exiting the portfolio.

This is why people talk about a fund's **vintage year**. A 2021 fund and a 2024 fund are not directly comparable because they bought companies in different market conditions, interest rate environments, and valuation cycles.

## How a PE Deal Works

Let's take a typical buyout deal.

The PE firm finds a company it wants to buy. This target company might come through:

- an investment bank running a sale process
- a founder conversation
- an industry relationship
- a proprietary sourcing effort
- a corporate carve-out
- another PE firm selling it

The deal process often looks like this:

```txt
Sourcing
  -> initial screening
  -> NDA
  -> CIM / management presentation
  -> first-round bid
  -> data room access
  -> due diligence
  -> investment committee approval
  -> final bid / LOI
  -> legal documentation
  -> signing
  -> closing
  -> ownership and value creation
  -> exit
```

Some terms:

**NDA**: Non-disclosure agreement. You sign this before seeing confidential information.

**CIM**: Confidential information memorandum. A fancy sales document prepared by the seller or banker.

**Data room**: A controlled document repository with financials, contracts, HR docs, customer data, legal docs, tech docs, security docs, and so on.

**LOI**: Letter of intent. A mostly non-binding document that says "we intend to buy under these rough terms", with some binding parts like exclusivity.

**Investment committee**: The group inside the PE firm that approves deals. If the IC says no, the deal does not happen.

**SPA**: Share purchase agreement. The legal contract for buying the shares.

**Closing**: The point where ownership actually transfers and money moves.

## Leveraged Buyouts

The classic PE transaction is the leveraged buyout, or LBO.

The idea:

> Buy a company using some equity and some debt.

Example:

```txt
Purchase price / enterprise value: 100m
Debt financing:                    60m
Equity from PE fund:               40m
```

The company is bought for 100m, but the fund only puts in 40m of equity. The rest is debt.

This is why leverage is powerful and dangerous.

If the company performs well, debt magnifies the equity return. If the company performs badly, debt can destroy the investment.

Important: the debt is usually at the portfolio company level. The portfolio company has to service it from its own cash flows. That is why PE firms care so much about EBITDA, cash conversion, working capital, and covenant headroom.

## A Simple LBO Example

Let's use a very simplified example.

The PE fund buys a B2B software company.

```txt
Entry
-----
EBITDA:          10m
Entry multiple:  10x EBITDA
Enterprise value: 100m

Debt:            60m
Equity:          40m
```

Over five years, the PE firm helps the company:

- increase prices
- improve sales execution
- reduce cloud costs
- acquire a smaller competitor
- professionalize finance and reporting

At exit:

```txt
Exit
----
EBITDA:          14m
Exit multiple:  11x EBITDA
Enterprise value: 154m

Remaining debt: 40m
Equity value:   114m
```

The fund invested 40m of equity and receives 114m back.

```txt
MOIC = 114m / 40m = 2.85x
```

The annualized return over five years is roughly:

```txt
IRR = (114 / 40) ^ (1 / 5) - 1
    = ~23%
```

Again, this is simplified. No fees, no taxes, no transaction costs, no management incentive plan, no working capital adjustment, no earn-out, no refinancing, no leakage, no disaster somewhere in year three.

But it shows the core PE math.

The return came from three levers:

1. **EBITDA growth**: 10m to 14m
2. **Debt paydown**: 60m debt to 40m debt
3. **Multiple expansion**: 10x entry multiple to 11x exit multiple

That is why PE people talk so much about:

- revenue growth
- margin expansion
- cash flow
- leverage
- entry multiple
- exit multiple
- value creation plan

## Enterprise Value vs Equity Value

This is one of the first finance distinctions worth learning.

**Enterprise value** is the value of the operating business, independent of how it is financed.

**Equity value** is what the shareholders get after debt and cash adjustments.

Simplified:

```txt
Enterprise Value = Equity Value + Debt - Cash

Equity Value = Enterprise Value - Debt + Cash
```

If you buy a company for 100m enterprise value and it has 30m debt and 5m cash, the equity purchase price is roughly:

```txt
100m - 30m + 5m = 75m
```

This matters in software because deal systems, valuation tools, and reporting tools often need to track both. If you mix them up, the numbers become nonsense very quickly.

## How PE Firms Create Value

There is a lazy version of the story:

> PE buys companies, loads them with debt, cuts costs, and sells them.

Sometimes that is unfortunately not too far from reality. But it is not the full picture.

Common value creation levers include:

**Revenue growth**

- better sales process
- new pricing
- cross-sell
- international expansion
- new product packaging

**Margin improvement**

- procurement savings
- cloud cost optimization
- lower support cost
- automation
- better utilization

**Add-on acquisitions**

- buy smaller competitors
- combine operations
- cross-sell into both customer bases
- create a larger platform company

**Management and governance**

- new CFO
- better reporting
- board discipline
- incentive plans
- 100-day plan after closing

**Capital structure**

- debt refinancing
- dividend recap
- pay down debt from cash flow

**Exit timing**

- sell when the company is performing well
- sell when market multiples are attractive
- sell to a strategic buyer that can pay more

For a tech company, value creation often gets very concrete:

- reduce infrastructure cost
- modernize legacy architecture
- improve gross margin
- reduce churn
- improve onboarding
- add usage-based pricing
- clean up security and compliance
- build a better data platform for reporting
- improve engineering throughput

This is why tech due diligence matters so much. A PE firm buying a software company wants to know whether the product is a scalable asset or a fragile pile of expensive promises.

## The Metrics People Use

There are many metrics, but these are the ones you should recognize in conversation.

**IRR**

Internal rate of return. Annualized return that accounts for timing of cash flows. Getting 2x in 3 years is better than getting 2x in 8 years. IRR captures that.

**MOIC**

Multiple on invested capital. If you invest 40m and get 100m back, MOIC is 2.5x. Simple and intuitive, but it ignores timing.

**DPI**

Distributions to paid-in capital. Cash returned to LPs divided by paid-in capital. DPI is important because paper gains are nice, but cash is cash.

**TVPI**

Total value to paid-in capital. Distributions plus remaining value, divided by paid-in capital.

```txt
TVPI = DPI + RVPI
```

**RVPI**

Residual value to paid-in capital. The value still sitting in unrealized portfolio companies.

**NAV**

Net asset value. The reported value of the remaining portfolio.

**Gross vs net**

Gross returns are before fund fees and carry. Net returns are after fees and carry. GPs often like to talk about gross deal returns. LPs care about net fund returns.

**EBITDA**

Earnings before interest, taxes, depreciation, and amortization. A common proxy for operating profitability. It is not cash flow, and people can "adjust" it quite creatively.

**ARR**

Annual recurring revenue. Especially important for SaaS businesses.

**Rule of 40**

For software companies: revenue growth percentage plus profit margin percentage. A company growing 30% with 15% margin has a Rule of 40 score of 45.

The [ILPA private equity glossary](https://ilpa.org/resources-tools/private-equity-101/private-equity-glossary/) is useful if you want a reference for many of these terms.

## The Words You Need at Lunch

Here is the short glossary that gets you surprisingly far.

**Platform**

The first main company in a strategy. Example: buy one dental software company as the platform, then acquire smaller dental software companies as add-ons.

**Add-on**

A smaller acquisition added to a platform company.

**Roll-up**

A strategy of buying many smaller companies in a fragmented market and combining them.

**Buyout**

Buying control of a company.

**Growth equity**

Minority or control investment in a growing company, usually with less leverage than buyouts.

**Sponsor**

Another word for the PE firm backing the deal.

**Portco**

Portfolio company. The company owned by the PE fund.

**Hold period**

How long the fund owns the company.

**Exit**

Selling the company or otherwise realizing the investment.

**Strategic buyer**

A company buying another company for strategic reasons. Example: Microsoft buying a software company.

**Sponsor-to-sponsor**

One PE firm sells a company to another PE firm.

**Secondary**

Buying or selling an existing fund interest or asset after the original investment.

**Continuation fund**

A vehicle used to hold an asset longer, often when the original fund is near the end of its life.

**Co-investment**

An LP invests directly alongside the fund in a specific deal.

**Carry**

The GP's share of investment profits, often 20%, after certain conditions are met.

**Management fee**

A fee paid to the manager, often used to pay salaries, sourcing, operations, and overhead.

**Hurdle**

A return threshold LPs must receive before the GP gets carry. The exact mechanics depend on the LPA.

**Waterfall**

The rules for distributing cash between LPs and GP.

**LPA**

Limited partnership agreement. The core fund contract.

**QoE**

Quality of earnings. Financial diligence that checks how real and sustainable earnings are.

**VCP**

Value creation plan. The plan for making the company more valuable during ownership.

**Covenant**

A promise in a debt agreement. Breaking covenants can create serious problems.

## A Lunch Translation Example

Suppose someone says:

> We like the platform, but entry is rich. The base case only works if we get the add-ons done, expand margin, and avoid multiple contraction.

Translation:

> The company is good, but expensive. The deal return is not attractive unless we buy more companies, improve profitability, and sell later at a valuation multiple that does not fall.

Or:

> DPI is still weak, but TVPI looks fine.

Translation:

> The fund has not returned much cash yet, but the remaining portfolio is marked at a good value. LPs may still be waiting for actual exits.

Or:

> The tech diligence flagged scalability and key-person risk.

Translation:

> The product may not handle growth well, and too much knowledge sits with one or two engineers. That can reduce valuation or kill the deal.

## What PE People Actually Do All Day

There is not one PE user. There are many.

**Deal team**

Sources deals, builds financial models, talks to bankers, runs diligence, writes investment committee memos.

**Partner**

Owns relationships, makes investment decisions, leads negotiations, sits on boards.

**Operating partner**

Works with portfolio companies on sales, pricing, technology, procurement, hiring, or other operational topics.

**Fund finance**

Handles capital calls, distributions, NAV, audit, LP reporting, fund accounting.

**Investor relations**

Raises new funds, communicates with LPs, prepares quarterly reports, responds to LP questions.

**Portfolio company management**

Runs the actual company. Provides metrics, board packs, budgets, forecasts, and strategic plans.

**Legal and compliance**

Handles fund documents, conflicts, regulatory obligations, side letters, approvals, disclosures.

**External advisors**

Lawyers, accountants, consultants, tech diligence providers, commercial diligence providers, tax advisors.

If you build a PE product, you need to know which of these users you are serving. A partner, a fund controller, and a portfolio CFO do not have the same workflow at all.

## What This Means for Product Builders

If you're building software in private equity, the domain is not just "finance CRUD".

There are a few patterns that show up again and again.

### 1. The Same Word Can Mean Different Things

"Company" can mean:

- target company
- portfolio company
- platform
- add-on
- seller
- buyer
- holding company
- operating company

"Investor" can mean:

- LP in a fund
- GP commitment
- co-investor
- lender
- buyer in an exit process

So domain modeling matters. You cannot just create a `Company` table and hope for the best.

### 2. Time and Versioning Are Everywhere

Every number needs context.

```txt
EBITDA = 14m
```

That is not enough.

You need:

- period: LTM as of Mar 31 2026?
- source: management report, audited financials, QoE adjustment?
- currency: USD, EUR, GBP?
- scenario: base case, upside case, downside case?
- version: before or after diligence adjustment?
- owner: who approved it?

In PE, "latest" can be dangerous. Latest according to whom? Latest actuals? Latest budget? Latest board-approved forecast? Latest deal-team case?

### 3. Excel Is Not Going Away

Many PE workflows still live in Excel and PowerPoint.

This is not because everyone is stupid. Excel is flexible, fast, and deeply embedded in finance work. The financial model is often the core artifact of a deal.

So a good PE product often needs:

- Excel import
- Excel export
- traceable formulas
- version comparison
- no silent rounding surprises
- support for manual overrides

If your product says "we replace Excel entirely", be careful. Sometimes the better product strategy is:

> Keep Excel where it is useful, but make the surrounding workflow auditable, collaborative, permissioned, and connected.

### 4. Permissions Are a First-Class Domain Problem

This is a big one.

PE data is extremely sensitive:

- acquisition targets
- valuations
- LP commitments
- side letters
- employee compensation
- debt terms
- customer contracts
- board materials
- unreleased financials

Access is not just admin vs user.

You may need:

- fund-level permissions
- deal-level permissions
- document-level permissions
- portfolio-company-level permissions
- LP-specific views
- wall-crossing controls
- external advisor access
- expiring data room access
- audit logs for every download

If you are building an AI feature, this becomes even more important. Retrieval must respect permissions at query time, not just at indexing time.

### 5. Auditability Matters

PE firms can be regulated investment advisers. Funds have LP agreements. Numbers go into investor reports. Decisions are approved by committees. Conflicts need disclosure.

So you need to know:

- who changed a number
- when they changed it
- why they changed it
- what the previous number was
- what source document supports it
- who approved it

This is basically event sourcing energy, but for finance workflows.

### 6. Documents Are the Interface

Private equity runs on documents:

- CIMs
- NDAs
- LOIs
- SPAs
- board packs
- financial models
- QoE reports
- legal memos
- LP reports
- side letters
- debt agreements

A lot of the domain knowledge is trapped in PDFs, Excel files, Word docs, emails, and PowerPoints.

That is why document intelligence and RAG are actually interesting here. But only if they come with citations, permissions, and deterministic workflows around them.

## A Simple Domain Model

If I had to start modeling a PE platform, I would not start with screens. I would start with the domain objects.

Very simplified:

```txt
Fund
  id
  name
  vintage_year
  strategy
  committed_capital

Investor
  id
  name
  type

Commitment
  fund_id
  investor_id
  committed_amount
  unfunded_amount

CapitalCall
  fund_id
  call_date
  due_date
  purpose

Deal
  id
  target_company_id
  stage
  deal_team
  enterprise_value
  equity_value

PortfolioCompany
  id
  acquisition_date
  ownership_percentage
  board_members

MetricObservation
  company_id
  metric_name
  value
  period
  scenario
  source_document_id
  approved_by

Distribution
  fund_id
  investor_id
  amount
  date
  type

Document
  id
  deal_id
  company_id
  confidentiality_level
  source
  version
```

This is still too simple, but it already shows the shape of the domain.

The hard parts are not the table names. The hard parts are:

- permissions
- versioning
- source traceability
- fund structures
- calculations
- workflows
- document extraction
- integration with Excel
- user trust

## Has AI Actually Changed Private Equity?

Yes, but not in the lazy "now everyone asks ChatGPT" way.

The more honest answer is:

> AI has started changing PE workflows, especially sourcing, diligence, portfolio operations, and internal productivity. But it has not automated investment judgement.

That distinction matters.

Bain's 2025 PE work described many firms as still being in test-and-learn mode, but also noted that a meaningful minority of portfolio companies had operationalized generative AI use cases and were seeing concrete results. Bain also reported that more than 60% of interviewed PE firms were using at least one tool for sourcing, screening, or diligence in its [2025 M&A generative AI report](https://www.bain.com/insights/generative-ai-m-and-a-report-2025/).

McKinsey's [Global Private Equity Report 2026](https://www.mckinsey.com/industries/private-capital/our-insights/global-private-markets-report/private-equity) also points to leading firms reflecting AI upside and downside directly in diligence, investment committee materials, and value creation plans.

So yes, this is real. But it is uneven.

## Where AI Helps in PE

### 1. Deal Sourcing and Screening

PE firms look at many more companies than they buy.

AI can help by:

- scanning company databases
- summarizing websites and filings
- identifying similar companies
- enriching company profiles
- detecting growth signals
- mapping markets
- finding add-on acquisition candidates

This is not magic. It is mostly better search, extraction, summarization, and classification over messy data.

But that is valuable because sourcing is a volume game.

### 2. Due Diligence

Diligence is document-heavy and time-constrained.

LLMs can help with:

- summarizing data room documents
- extracting contract terms
- comparing customer contracts
- finding change-of-control clauses
- summarizing customer call transcripts
- extracting security issues from tech reports
- creating question lists for management
- mapping open diligence requests

This is one of the strongest use cases because the input is messy text and the output is often a structured memo, checklist, or risk list.

But the output needs citations. A diligence answer without source references is not good enough.

### 3. Investment Committee Materials

IC memos are long and repetitive. They combine:

- market overview
- company description
- investment thesis
- financial model summary
- risks
- diligence findings
- value creation plan
- exit scenarios

AI can help draft and update these materials.

But again, it should not invent. The useful version is:

> "Draft the market section using these approved sources and cite every claim."

Not:

> "Write a confident investment memo from vibes."

### 4. Portfolio Monitoring

Once the fund owns companies, it needs reporting.

AI can help detect:

- margin changes
- churn spikes
- budget misses
- covenant risks
- hiring delays
- customer concentration problems
- anomalies in board packs

Here LLMs are usually not enough alone. You want deterministic data pipelines and metrics first, then AI on top for explanation and triage.

### 5. Portfolio Value Creation

This is probably the biggest AI impact.

PE firms can push AI adoption across portfolio companies:

- customer support automation
- sales enablement
- marketing content
- code generation
- QA automation
- back-office automation
- document processing
- pricing analysis
- customer success workflows
- product features with AI inside

This is where AI becomes more than "a tool for the deal team". It becomes part of the value creation plan.

If a PE firm owns 40 software companies, it can learn what works in one and spread it to others. That portfolio-level learning loop is powerful.

### 6. Tech Due Diligence Itself

If the target is a software company, AI changes the diligence questions.

The deal team now wants to know:

- Does AI threaten this product?
- Can competitors replicate the product faster now?
- Can the company improve engineering productivity with AI?
- Is the codebase ready for AI-assisted modernization?
- Is the data clean enough to build AI features?
- Are there privacy, IP, or security risks?
- Is the product's moat still real?

This is a big change. AI is no longer just a tool used during diligence. AI is also a topic inside diligence.

## Where AI Does Not Replace People

AI does not replace:

- relationships with founders and bankers
- negotiation judgement
- investment committee accountability
- board work
- management assessment
- legal judgement
- final valuation decisions
- understanding whether the market thesis is actually right

Also, PE is full of high-stakes numerical work. You do not want an LLM to be the source of truth for IRR, waterfall, debt schedule, covenant compliance, or management fee calculations.

The pattern I would trust is:

```txt
LLM: extraction, summarization, explanation, draft generation
Code: calculations, permissions, workflow state, audit logs
Human: judgement, approval, accountability
```

That is the architecture.

## Building AI Products for PE

If you build an AI feature for PE, I would care about these things first.

**Permission-aware retrieval**

Do not index a data room once and then let everyone query everything. Access control must be enforced when retrieving context.

**Citations**

Every generated answer should point back to the exact document, page, cell, or source record.

**Deterministic calculations**

Use real code for finance math. Let the LLM explain the result, not calculate the official result.

**Human approval**

AI can draft an IC memo section. A human approves it. AI can suggest diligence questions. A human sends them.

**Versioning**

When source documents change, generated outputs need to know which version they used.

**Excel integration**

If your AI product cannot understand, export, or reconcile with Excel, adoption will be harder.

**Evaluation**

You need test sets. Example: 100 contracts with known change-of-control clauses, 100 CIMs with known revenue numbers, 50 board packs with known KPIs. Otherwise you cannot measure whether extraction works.

This is especially important because PE users will not tolerate "mostly right" for numbers.

## Common Mistakes When Building PE Software

### Treating It Like a Normal CRM

Deal sourcing can look like CRM, but PE workflows are not just sales pipelines.

You need deal stages, documents, approvals, valuations, relationship history, conflicts, NDAs, data rooms, IC materials, financing terms, and follow-up tasks.

### Ignoring Fund Structures

A PE firm can manage many funds. A deal might be owned by one fund, multiple funds, a co-invest vehicle, and management rollover.

If your model assumes "one company belongs to one fund", it may break quickly.

### Mixing Gross and Net

Gross deal return is not net LP return. This mistake is everywhere in weak finance software.

### Missing As-Of Dates

Metrics without periods are dangerous.

```txt
ARR: 50m
```

As of when?

### Hiding the Source

If a number appears in a dashboard, the user will ask:

> Where did this come from?

Your product should answer that immediately.

### Underestimating Trust

PE users are often skeptical of new systems because a wrong number can be embarrassing or expensive.

The product has to earn trust through traceability, exports, permissions, and boring correctness.

## Wrapping Up

Private equity is not that hard to understand at a high level.

A PE firm raises a fund from LPs. The GP manages it. The fund buys companies, often using debt. The PE firm tries to make those companies more valuable through growth, operational improvement, add-on acquisitions, better management, and better capital structure. Then it exits and distributes money back to LPs and, if returns are good enough, to the GP through carry.

The complexity is in the details:

- fund structures
- incentives
- leverage
- valuation
- legal documents
- capital calls
- distributions
- reporting
- permissions
- diligence
- portfolio operations

For tech people, the most important insight is this:

> PE is a workflow-heavy, document-heavy, permission-heavy, number-heavy domain.

That makes it painful to build for, but also interesting.

AI and LLMs are genuinely useful here, especially for sourcing, diligence, portfolio monitoring, and value creation. But the winning architecture is not "let the model do finance". It is deterministic systems for numbers and permissions, plus AI for extraction, search, drafting, and explanation.

If you understand that, you already understand a lot more than the average person nodding along at lunch.
