# Using the HeFu Model Workbench

The [HeFu model workbench](https://www.hefu.hk/models) is the no-code way to
explore everything this API can do before you write any code: full-modality
online debugging (text, image, video and voice), scenario presets, live code
generation, and a private results center.

## What it is for

- **Pick your models fast.** Filter the live catalog, compare latency and
  pricing, and run the same prompt across several models side by side — the
  exact model IDs you see there are the ones you pass to `model=` in the API.
- **Debug prompts and parameters.** Tune temperature, system prompts and
  multimodal inputs interactively, then copy the generated code snippet
  straight into your project (Python, Node.js or curl).
- **Scenario presets.** Jump straight into common tasks (marketing copy,
  cross-border e-commerce listings, HR recruiting, code review) instead of
  assembling prompts from scratch.
- **Private results center** (`/dashboard/results`). Every run — including
  async video and audio jobs — lands in your private results center where you
  can review, rename, and continue the work later. Nothing is lost when you
  leave the page.
- **Team quotas.** Organization owners can create sub-accounts with per-user
  quotas, so a small team shares one balance without sharing one key.

## Typical workflow

1. Sign in at <https://hefu.hk>, open the workbench, and shortlist two or
   three models for your use case.
2. Iterate on the prompt until the output is right; use the live code pane to
   export the call.
3. Move the exported call into a script (see the [quickstart](../quickstart)
   examples) and set a client timeout ≥120 s with exponential backoff on
   429/5xx.
4. Long-running generations (video, batch images) stay visible in the results
   center — poll the job endpoint shown in the OpenAPI contract
   (<https://hefu.hk/openapi.yaml>) or pick the results up later.

## Related guides

- [Cline setup](cline-setup.md) — point a coding assistant at the same endpoint
- [Open WebUI setup](open-webui-setup.md) — self-hosted chat UI
- [Dify setup](dify-setup.md) — no-code LLM app platform
