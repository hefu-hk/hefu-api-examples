# DramaStudio Short-Drama Workflow

[DramaStudio](https://drama.hefu.hk/) is HeFu's managed, no-code short-drama workspace. It is separate from the unified model API quickstarts: use it when you want the production stages organized for you rather than selecting models and orchestrating calls yourself.

## Before you start

1. Create or sign in to your [HeFu account](https://hefu.hk).
2. Open DramaStudio and authorize the application through HeFu OAuth.
3. Confirm the shared-wallet balance and current usage terms. Generation is billed by actual model usage; basic/standard/premium are model-capability choices, not bundled usage allowances.

## Production flow

1. Create a project and generate the script and initial assets.
2. Edit the script and adjust the editable storyboard.
3. Review generated shots with your team and regenerate only the material that misses your requirements.
4. Produce visual and voice assets.
5. Compose the timeline and review subtitles.
6. Export the episode package.

Current deliverables are an MP4 episode, a ZIP of generated assets, SRT/VTT subtitles, a storyboard CSV, and a review report. Continue in your own editing tools if you need other formats.

## Review boundary

Generated output is a draft, not a guarantee of distribution quality, originality, or copyright clearance. Output ownership and permitted use depend on applicable law and the upstream terms that apply to your project. Review the script and assets manually before publication or commercial use.

## Related paths

- [DramaStudio tutorial on the HeFu blog](https://blog.hefu.hk/en/blog/dramastudio-ai-short-drama-creation-tutorial)
- [Unified model API quickstart](../quickstart/python_openai_sdk.py) — for custom applications that need direct model control.
- [Third-party app integration](../app-integration/README.md) — for OAuth-based application workflows, not a substitute for the DramaStudio UI.
