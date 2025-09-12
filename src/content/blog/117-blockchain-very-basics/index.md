---
title: "Blockchain: The Very Basics, ELI5"
summary: "Absolute basic and just semi-correct breakdown of blockchain, kind of like an ELI5"
date: "April 03 2021"
draft: false
tags:
  - Blockchain
---

# Blockchain: The Very Basics, ELI5

So the idea is this - imagine a chain of blocks where each block is cryptographically linked to the previous one. It's like a digital ledger that's really, really hard to tamper with.

## What's Inside a Block?

Each block has these key components:

- **Previous Block Hash** - a unique fingerprint of the previous block
- **Nonce** - a number that miners have to guess (more on this below)
- **Data** - the actual information being stored (transactions, etc.)
- **Current Block Hash** - the unique fingerprint of this block

## How the Chain Works

Each previous block hash must match the current block hash of the preceding block. The formula looks something like this: 

```
Block Hash = SHA256(Previous Hash + Nonce + Data + Timestamp)
```

This creates an unbreakable chain - well, almost unbreakable.

## Mining: The Hard Part

The mining is difficult, and it works like this: you guess a nonce (that's the number) and hope that the formula above produces a hash that starts with a certain number of zeros (like `0000abc123...`). Only if that's the case, then you may add your block to the chain.

You need to iterate millions, sometimes billions of times until you find the right nonce. On average, Bitcoin miners try about 7 quintillion combinations per second across the entire network.

So that's costly - both energy and time expensive by design.

## Why This Actually Works

Well, doing one block is fine, but if you change one block's data, then the hash will no longer match the formula, so everyone sees it's manipulated and thus your change won't be accepted. You could of course manipulate all following hashes as well, but that's basically an impossible amount of work - you'd need more computing power than the rest of the network combined.

## Special Blocks

**Genesis Block**: This is at the beginning of every blockchain - the first block that has no previous hash to reference.

## Where Is This Thing Stored?

The blockchain (the entire thing) is stored on thousands of computers around the world. Each participant has a copy of the entire ledger. When someone wants to add a new block, the majority of the network has to agree it's valid.

This distributed storage is what makes it so secure - you can't just hack one server, you'd need to hack thousands simultaneously.

## Beyond Cryptocurrency

Now, why is this groundbreaking? It's used in way more places than just crypto:

- **Supply Chain Tracking** - you can trace where your coffee beans came from
- **Digital Identity** - secure, tamper-proof identity verification
- **Smart Contracts** - automated agreements that execute themselves
- **Voting Systems** - transparent, verifiable elections
- **Medical Records** - secure, shareable patient data
- **Real Estate** - property ownership records that can't be forged

## The Trade-offs

Sure, blockchain is cool, but it's not perfect:

- **Energy Consumption** - Bitcoin uses as much electricity as some countries
- **Speed** - It's slow. E.g. Bitcoin processes about 7 transactions per second (Visa does 65,000)
- **Storage** - every participant needs to store the entire history (doesn't mean every Bitcoin user needs to though)
- **Complexity** - it's not exactly user-friendly for your average person

But for problems where you need trust without a central authority, blockchain can be pretty revolutionary.

## Text Form Summary

So a blockchain is a decentralized, immutable ledger where each info is saved in blocks. Those blocks are chained via hashes and this mechanism makes the ledger secure.

There are different mechanisms to reach _consens_, like Proof of Work (what I said above, used for BTC (Bitcoin)), Proof of Stake (Ethereum), and more.

There are public blockchains as well as private ones. BTC and Ethereum are public ones for examples.

While this technology provides amazing benefit when it comes to safety, decentralization (no single or few parties are in control), trust, there are clear tradeoffs. It's slow (transactions per second, again BTC can do about 7 per second), it uses tremendous energy ressources, it's complex, and it brings questions regarding regulation.

That being said, there are clear use cases in the economy:
- cryptocurrencies
- web3
- DeFi
- Digital Identity & SSI
- Supply Chain? kinda, see walmart example. but most dont do it, because the use doesnt warrant the complexity, other software can solve the issues too. Also IBM food trust


## Consensus Mechanisms

So how do all these computers actually agree on what's valid? That's where consensus mechanisms come in - think of them as the rules of the game.

**Proof of Work (PoW)** - What Bitcoin uses. Miners compete to solve math puzzles. Winner gets to add the block and earn rewards. It's like a lottery where more computing power = more tickets.

**Proof of Stake (PoS)** - What Ethereum switched to. Instead of burning electricity, validators put up money as collateral. If they validate bad transactions, they lose their stake. More efficient, but some argue less decentralized.

From a business consultant perspective (think Capgemini solution architect), here's what matters:

- **PoW**: More secure, battle-tested, but terrible for ESG goals
- **PoS**: Energy efficient, faster, but newer and potentially more centralized
- **Private/Consortium**: Custom rules, faster, but defeats the "trustless" purpose

Choose PoW for maximum security and decentralization. Choose PoS for sustainability and speed. Choose private blockchain when you just need tamper-proof records within known parties.
## Strategic Business Discussions - Opportunities vs. Challenges

Here's where you need to show you can think about real-world implications, not just the tech:

### Opportunities

**New Business Models**: Tokenization is huge. BlackRock is testing tokenized funds, people are tokenizing real estate and art. Suddenly you can own a fraction of a Picasso or get exposure to commercial real estate with $100.

**Trust Infrastructure**: Self-Sovereign Identity (SSI) could revolutionize bureaucracy. Instead of remembering 20 passwords and carrying 10 different IDs, you have one wallet that proves who you are.

**Efficiency Gains**: Automated document processes. Think customs papers, insurance claims, supply chain documentation - all automatically verified and processed.

### Risks & Challenges

**Regulation**: EU's MiCA (Markets in Crypto Assets) brings legal clarity, but also compliance costs. Companies need to navigate a patchwork of regulations across different countries.

**Adoption Gap**: Many pilots never scale. Remember IBM's TradeLens for shipping? Promised to revolutionize global trade, but couldn't get enough participants on board.

**Scaling Issues**: Ethereum does ~15 transactions per second, Bitcoin ~7. Compare that to Visa's 65,000 TPS. Layer-2 solutions like Polygon and Optimism help, but add complexity.

**Energy Concerns**: Proof-of-Work blockchains face major ESG criticism. Try explaining Bitcoin's carbon footprint to your sustainability team.

### Future Trends

**CBDCs**: China's Digital Yuan is already live, EU is testing Digital Euro, Nigeria launched eNaira. Governments want the benefits of blockchain without losing monetary control.

**AI Convergence**: Blockchain as audit trail for AI outputs. Who created this prompt? What training data was used? Blockchain can create tamper-proof logs.

**Enterprise Consortiums**: More private blockchains for specific industries. Financial consortiums, Industry 4.0 manufacturing networks.

## Blockchain + IoT - Why It's Interesting (But Not Really Happening Yet)

**The Problem Blockchain Could Solve**: IoT devices generate massive amounts of data, often distributed and requiring trust. Who guarantees this data is authentic? Blockchain offers tamper-proof, immutable ledgers.

**Example Use Cases That Sound Great**:

- **Machine Pays Machine**: Your car automatically pays tolls or charging stations via smart contracts
- **Supply Chain & Asset Tracking**: Sensors report temperature/humidity → blockchain stores data immutably for pharma cold chains or food safety
- **Predictive Maintenance**: IoT reports usage → blockchain logs service history → reliable warranty claims

**But Here's the Reality**: This idea sounds amazing, but it's barely used anywhere in practice. Why?

**Why It's Not Working Yet**:

- **Complexity Overkill**: Most IoT data doesn't need blockchain-level immutability. Regular databases work fine and are way simpler
- **Cost vs. Benefit**: The overhead of blockchain often outweighs the benefits for typical IoT use cases
- **Integration Nightmare**: Getting IoT devices, blockchain networks, and existing enterprise systems to play nice is brutal
- **Performance Issues**: IoT generates tons of data, blockchain is slow. That's a problem
- **Energy Concerns**: Adding blockchain to already power-constrained IoT devices doesn't make sense

**The Bottom Line**: Great concept, but traditional cloud databases with proper security usually solve the same problems with much less hassle. Blockchain + IoT is still mostly conference slides and pilot projects.