/**
 * HeFu quickstart with the official OpenAI Node SDK.
 *
 * HeFu exposes an OpenAI-compatible API, so the only change versus a stock
 * OpenAI setup is `baseURL` — every other call stays identical.
 *
 * Setup:
 *   npm install openai
 *   export HEFU_API_KEY="sk-hefu-..."
 *   node quickstart/node_openai_sdk.mjs
 */

import OpenAI from 'openai';

// Read the key from the environment; never hard-code keys in source.
const apiKey = process.env.HEFU_API_KEY;
if (!apiKey) {
  console.error('HEFU_API_KEY is not set. Export it first, e.g.: export HEFU_API_KEY=sk-hefu-...');
  process.exit(1);
}

const client = new OpenAI({
  apiKey,
  baseURL: 'https://api.hefu.hk/v1', // the only option that differs from a stock OpenAI client
});

// A spread of flagship models available through the same endpoint and key.
// Model IDs change over time — see https://www.hefu.hk/models for the live
// catalog (as of 2026-11).
const MODELS = ['kimi-k3', 'claude-opus-4.5', 'gpt-6.1-terra'];

for (const model of MODELS) {
  const response = await client.chat.completions.create({
    model,
    messages: [
      { role: 'system', content: 'You are a concise assistant.' },
      { role: 'user', content: 'In one sentence, what is an API gateway?' },
    ],
    temperature: 0.3,
    max_tokens: 120,
  });
  console.log(`--- ${model} ---`);
  console.log(response.choices[0].message.content);
  console.log(`(tokens: ${response.usage.total_tokens})\n`);
}
