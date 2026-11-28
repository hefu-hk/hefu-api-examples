/**
 * HeFu quickstart with the official OpenAI Node SDK.
 *
 * Setup:
 *   npm install openai
 *   export HEFU_API_KEY="sk-hefu-..."
 *   export HEFU_MODEL="a-current-model-id"
 *   node quickstart/node_openai_sdk.mjs
 *
 * The example makes one real, billable chat request.
 */

import OpenAI from 'openai';

const apiKey = process.env.HEFU_API_KEY;
if (!apiKey) {
  console.error('HEFU_API_KEY is not set. Export it first, e.g.: export HEFU_API_KEY=sk-hefu-...');
  process.exit(1);
}

// Replace the default when the live catalog changes.
const model = process.env.HEFU_MODEL || 'deepseek-v4-flash';
const client = new OpenAI({
  apiKey,
  baseURL: 'https://api.hefu.hk/v1',
});

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
console.log(`(tokens: ${response.usage.total_tokens})`);
