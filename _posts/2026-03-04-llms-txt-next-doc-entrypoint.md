---
title: "llms.txt Is Not the End, but It Might Be the Next Documentation Entry Point"
excerpt: "When agents become the primary readers, llms.txt shifts from a small feature to a practical entry layer for reliable AI-facing documentation."
tags: [llms, documentation, agents, mcp, api]
---

While building AgentPort, one thing became immediately clear:
we used to write docs assuming humans were the default readers.
For a long time ahead, more and more of those readers will be agents.

At first, I treated `llms.txt` as a minor feature. Later, I started seeing it as a signal.
It was proposed on September 3, 2024, and as of March 2026 it is still mostly a de facto
community standard, not a formal ISO or IETF standard.

That does not reduce its value. It solves a practical problem:
help the model know where to look first and what to read.

Why do I think this direction matters?
Because agent workflows are changing. They are no longer about reading webpages for humans.
They are increasingly about calling information and tools directly inside execution flows.

At that point, the expensive cost is not model inference itself.
The expensive part is integration cost and reliability cost.
If every website needs one-off integration work, this will never scale.

So this is the conclusion I trust more now:
what unlocks useful agents is not only stronger models, but infrastructure that lets models
retrieve correct information reliably.

- `llms.txt` is the entry point.
- MCP and APIs form the invocation layer.
- Continuous updates and traceability are the foundation.

Whoever connects these three layers well gets closer to a truly usable agent era.
