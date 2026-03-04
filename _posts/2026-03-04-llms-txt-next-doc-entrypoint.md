---
title: "llms.txt Isn't the End, but It Might Be the Front Door for Next-Gen Docs"
excerpt: "Building AgentPort changed how I think about docs: agents need a reliable entry point, and llms.txt is a practical start."
tags: [llms, documentation, agents, mcp, api]
---

While building AgentPort, one thought kept coming back:
we used to write docs with humans as the default reader.
For the next few years, more and more of those readers will be agents.

I first treated `llms.txt` as a minor feature.
Now I see it more as a signal.

It was proposed on September 3, 2024, and as of March 2026 it is still mostly a de facto
community standard, not a formal ISO or IETF standard.
That does not make it less useful.

Its value is practical:
it helps the model know where to start and what to read first.

Why this matters:
agent workflows are changing from "read this page for a person"
to "call information and tools directly inside a running flow."

When that shift happens, model inference is not the biggest cost.
The bigger costs are integration and reliability.
If every website needs one-off integration work, this will never scale.

So this is the conclusion I trust more now:
the future is not only stronger models.
It is infrastructure that helps models retrieve correct information reliably.

- `llms.txt` is the entry layer.
- MCP and APIs are the invocation layer.
- Continuous updates and traceability are the foundation.

Whoever connects these three layers well gets closer to a truly usable agent era.
