# Application-Layer Fallback Routing

One gateway doesn't remove the need for resilience: individual models can rate-limit (429), overload (5xx), or drift in latency. A small **fallback chain** in your application keeps requests succeeding by walking down an ordered list of models — all through the same HeFu endpoint and key.

Runnable implementation: [examples/fallback.py](../examples/fallback.py)

## The chain

```text
deepseek-v4-flash  →  qwen3.6-plus  →  kimi-k2.6
     (fast/cheap)      (balanced)      (strong last resort)
```

Order by your priorities: cheapest-first minimizes spend; strongest-first maximizes first-try quality. Any [catalog](https://www.hefu.hk/models) IDs work — the chain below is an example, not a requirement.

## When to fall back vs. when to retry

Not every error should hop to the next model:

| Failure | Action | Why |
|---|---|---|
| `429` rate limit / quota | Retry same model with backoff, then fall back | Often transient; a short wait may be cheaper than switching |
| `5xx` server error | Fall back (with one quick retry) | Upstream is unhealthy; waiting rarely helps immediately |
| Network timeout / connection error | Retry, then fall back | Could be either side |
| `4xx` other than 429 (400, 401, 403, 404) | **Fail immediately** — never fall back | Your request is wrong; every model will reject it identically |

The key rule: **only fall back on retryable infrastructure errors, never on client errors.** A 400 that means "your payload is malformed" will follow you down the whole chain and turn one bug into N wasted calls.

## Design notes

- **Bounded retries:** per model, retry at most 1–2 times with exponential backoff plus jitter (e.g. 0.5s, 1s × random factor) before moving on.
- **Total deadline:** cap the whole chain (e.g. 30s). A fallback chain that can burn minutes is worse than a fast failure.
- **Report the winner:** return which model actually answered (the example attaches `x_hefu_fallback` metadata) so you can monitor how often the primary degrades.
- **Keep quality in mind:** fallback models are *different models*. For user-facing features, log or surface degradations; for background jobs, silent fallback is usually fine.
- **Gateway-side alternative:** if you don't want fallback logic in every app, put it in a thin proxy of your own (or mirror it in a workflow tool — see the n8n/Dify guides) so apps keep calling one model name.

## Example output

```text
$ python examples/fallback.py
[answer via deepseek-v4-flash after 1 attempt(s)]
An API gateway is a single entry point that routes, authenticates, ...
```

## Further reading

- [HeFu docs](https://www.hefu.hk/docs) — error codes and rate-limit details
- [HeFu pricing](https://www.hefu.hk/pricing) — pick chain order with real numbers
- [AI API gateway for developers](https://blog.hefu.hk/en/blog/ai-api-gateway-for-developers) — background on the gateway pattern
