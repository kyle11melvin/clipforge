# Prompt to open the Switchboard launch work (paste as the first message in a session on kyle11melvin/switchboard)

SWITCHBOARD — TAKE IT TO THE APP STORE

I'm Kyle Melvin. I don't write code; you and I build things together. Today's job is the start of a real
launch: get Switchboard into the iOS App Store as a paid subscription app, and do it with me as the only
human on the project. Read the whole repo before you say anything, then give me the audit described at the
bottom.

WHAT SWITCHBOARD IS
One question in. Switchboard sharpens the prompt, picks the AI models best suited to the question, gets
their independent answers, compares and challenges them (strong points, weak points, contradictions), and
combines the best into one top answer. The pitch: "One question. The right AIs. One top answer." Speak to
everyday users, never developers. Never claim the answer is guaranteed correct; claim it was checked against
other models.

WHAT ALREADY EXISTS ELSEWHERE
The repo kyle11melvin/clipforge holds the finished 32-second commercial
(videos/switchboard/v4/Switchboard-Commercial-V4.mp4, composition in graphics/switchboard-v4/), the real app
icon (graphics/siri-post/icons/switchboard.png, upscaled at graphics/switchboard-v4/logos/switchboard-icon.png),
official provider logo SVGs (graphics/switchboard-v4/logos/), and a renderer that can produce App Store
screenshots later. Add that repo to the session when you need those assets. The example question used
everywhere is "I built an app. How do I turn it into a profitable business?" and the four prompt areas are
Market demand, Competition, Pricing, Launch strategy. Selected models in the example are Claude, Perplexity
and Gemini.

HOW WE WORK
- I review on my phone. Deliver anything visual on a private artifact page with a Save button and stills
  before a full build. Keep replies short. My messages are dictated and sometimes garbled; read for intent
  and confirm wording that ships.
- I have a MacBook and an iPhone. I will create the Apple developer account, hold every API key and payment
  account, and press submit in App Store Connect. You never store my secrets in the repo; tell me exactly
  what to paste where, in my own environment.
- Ship a whole step, then list what is missing. Don't ask permission for reversible work.
- Don't pad the scope. No new product features beyond the pipeline above, accounts, history, subscriptions
  with usage caps and overage packs, and what Apple requires.

BUSINESS MODEL (my current thinking, challenge it if the numbers say otherwise)
Subscription. Two tiers to propose: a cheaper plan on fast models and a premium plan on the strongest models
with the full compare-and-challenge treatment, each with a monthly question cap and paid question packs
above the cap so a heavy user never costs me money. Every question is roughly five model calls (sharpen,
three answers, compare/combine), so price from the real per-question cost at current published rates, after
Apple's cut.

THE PLAN WE AGREED
1. Audit (this session): decide keep or rebuild.
2. Core (about two weeks): backend that holds the keys and runs the pipeline, usage caps, one clean
   ask-and-answer screen, cloud builds so I can test on my phone.
3. Product (about two weeks): accounts, history, the "what was challenged" view, subscriptions and overage
   via a billing layer that is free until revenue.
4. Launch prep (one to two weeks): TestFlight, polish from my notes, listing copy, screenshots, privacy
   policy and terms, submit.
5. Apple review and fixes.
Target: live in six to nine weeks. Then marketing with the commercial and my content.

THE AUDIT I WANT BACK TODAY
- What is in this repo: platform, how it was built, what runs today, what is broken.
- Where API keys live now and whether anything secret is committed. If it is, say so first and tell me how
  to rotate it.
- Keep or rebuild, with one paragraph of reasons.
- The exact list of things only I can do, in order, with what each one costs.
- The first build step you would start right after I say go.
