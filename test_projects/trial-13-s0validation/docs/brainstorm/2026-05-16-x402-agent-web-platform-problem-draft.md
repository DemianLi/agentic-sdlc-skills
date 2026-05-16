## Chosen Problem Framing

**Lens C — Missing Abstraction**

The real problem is that there is currently no way to represent "a website's data" as an agent-callable service with clear pricing and access rules — so developers are forced to rely on brittle scraping or expensive browser automation every time they need web data, and every new agent project rebuilds the same unstable infrastructure from scratch.

---

## Problem Space Map

| Dimension | Question | Answer |
|-----------|----------|--------|
| **Who** | Who specifically suffers? | AI agent developers; anyone who wants to collect web data through agent tools |
| **Frequency** | How often does it occur? | Every new agent project that needs external web data |
| **Cost** | Cost of doing nothing? | Repeated scraping infrastructure per project; excessive token consumption via Browser MCP; frequent blocks from anti-scraping defenses; computer use too immature for reliable automation |
| **Workaround** | What do people do today? | Browser MCP (expensive, token-heavy); self-built web scrapers (brittle, easily blocked) |
| **Broken thing** | What specifically breaks down? | No standard agent-friendly interface on websites; no shared protocol for agents to access web content; computer use not mature; each developer reinvents the wheel |

---

## Rejected Framings

- **Lens A (User Pain)**: "Every agent project rebuilds the same data-access infrastructure" — rejected because this is a symptom, not the root cause. Even if shared tooling existed, the underlying gap (websites not designed for agents) would remain.
- **Lens B (System Inefficiency)**: "The web is designed for human browsers, not agents, with no standard machine-readable interface layer" — not rejected outright, but too broad. Lens C is more specific and directly points to the business model and technical solution space (x402 + service description format + agent discovery).

---

## Open Questions

1. **x402 integration**: How does x402 specifically fit in? What does an "x402-enabled website" look like from the agent's perspective — is it a header, an endpoint, a manifest file?
2. **Service description format**: How does an agent discover what a website exposes? Is there a standard schema (like OpenAPI, but for agent-callable web content)?
3. **Conversion mechanism**: Who converts existing websites? Does the website owner implement something new, or is there a proxy/middleware layer that wraps any website?
4. **Pricing model**: Who sets the price per data access? Website owner? Platform? Is this per-page, per-field, per-query?
5. **Legal/compliance**: What are the implications of automated, paid data access — does a payment change the legal status of scraping?
6. **Agent discovery**: How does an agent know which websites are available on the platform, and what data they expose?

---

## What This Is NOT

- **Not a web scraping service** (like ScrapingBee, Apify) — those are human-API tools without agent-native design or payment protocol
- **Not a general-purpose browser automation tool** — the goal is structured data access, not visual browser control
- **Not a website building platform** — existing websites are the target, not new ones
- **Not a replacement for REST APIs** — websites that already have good APIs don't need this
- **Not limited to any single vertical** — the platform should be website-agnostic
- **Not a cryptocurrency speculation product** — x402 is the plumbing, not the value proposition
