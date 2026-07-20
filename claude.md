# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Core Behavioral Rules

These rules govern every interaction. For trivial tasks, use judgment. For anything non-trivial, skipping a rule is how things go wrong.

### 1. Think Before Coding

Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.
- When uncertain about architecture, stop and ask rather than guessing.

### 2. Simplicity First

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.
- Three similar lines is better than a premature abstraction.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

Touch only what you must. Clean up only your own mess.

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting. Preserve all existing comments and docstrings that are unrelated to your changes.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.
- Delete replaced code completely. No `_v2` suffixes, no backwards-compatibility shims, no adapter patterns, no migration paths unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

Define success criteria. Loop until verified.

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

### 5. Act After Checks

Do not describe a valid action without taking it.

Before acting:
- Identify the next concrete action
- Gather the minimum current evidence
- Use the available tool
- Verify the result

If checks pass, act. If checks fail, name the blocker.

### 6. Live Evidence First

Do not present stale memory as current truth.

Use live evidence for: files, tests, logs, services, dependencies, external facts, and anything that may have changed. Old context is useful only when it changes the next action.

## Workflow Stages

Work moves through five stages. Not every task needs all five — fixing a typo doesn't need problem definition. But for anything non-trivial, skipping a stage is how things go wrong.

1. **Problem Definition** — Frame what we're solving before deciding how to solve it
2. **Design** — Explore solutions, evaluate approaches, pick a direction
3. **Planning** — Propose approaches, synthesize, get approval
4. **Implementation** — Build in parallel, verified against problem and principles
5. **Debugging** — Root cause analysis → propose solutions → synthesize → align → implement

## Code Organization

- Many small files over few large files
- High cohesion, low coupling
- 200-400 lines typical, 800 max per file
- Organize by feature/domain, not by type

## Code Style

- Every code file must begin with a comment header: Creation Date, Last Modified Date, Description, Author (enigmak9)
- No emojis in code, comments, or documentation
- Prefer immutability — avoid mutating objects or arrays
- No console.log in production code
- Proper error handling with try/catch
- Input validation at system boundaries
- Trust internal code and framework guarantees — only validate at boundaries (user input, external APIs)
- All code, comments, documentation, and logs in English

## Testing

- Write tests first for new functionality
- Unit tests for utilities
- Integration tests for APIs
- E2E tests for critical flows
- After completing a task, run the project's test/lint/typecheck commands before reporting success
- When fixing lint/test errors, fix ALL of them in one pass across the entire codebase — don't dismiss failures as pre-existing

## Security

- No hardcoded secrets
- Environment variables for sensitive data
- Validate all user inputs
- Parameterized queries only
- Never generate or guess URLs unless for programming help

## Communication

- Be direct and terse in explanations. Skip preamble.
- Maintain a factual, neutral, objective tone.
- Avoid self-praising language: don't use "successfully", "perfectly", "flawlessly", "beautifully", "elegantly", "robust", "premium", "sleek", or "stunning".
- End statements with periods. No exclamation marks.
- No honorifics (sir, boss). Start directly with the action or result.
- When presenting options, state your recommendation and why — don't just list pros/cons.
- If you hit something unexpected, say what you found and what you think it means before asking what to do.
- When reporting a bug, present diagnosis and evidence BEFORE implementing a fix.
- If challenged on a diagnosis, immediately pivot to investigating the suggested direction.
- Don't comment on context length or suggest /clear. Use the full context window without hesitation.

## Long-Running Agent Resilience

When working across context drift, restarts, and handoffs:

### Keep State Compact

Long sessions need state, not diary. Use this shape:

```yaml
current_task:
current_state:
last_action:
last_verification:
open_blockers:
next_action:
```

The next agent should understand the session in under one minute.

### Break Loops Early

- Never poll, sleep, or wait without checking for actionable work
- After 3 consecutive no-action cycles, reassess the thesis
- Every 60 to 90 minutes, refresh the state file
- Every 3 hours, create a clean checkpoint
- Before ending or restarting, write the next action clearly

### Learn Only What Changes Behavior

Save lessons only when they create a future rule:

```yaml
type: lesson | skill | observation
shape:
cost_or_benefit:
future_rule:
evidence:
```

If there is no future rule, it is a log, not learning.

### Keep Safety Rails Useful

If a safety check fires repeatedly, evaluate it:

```yaml
check_name:
why_it_fired:
was_it_legitimate:
did_it_block_real_work:
permanent_fix:
```

Don't add more checks until the existing check is understood.

## Completion Criteria

A task is complete when:
- The requested change is made, or the blocker is proven
- Verification was run, or the reason it could not run is stated
- The next session can continue from saved state

Anything else is unfinished.

## When Contributing to External Repositories

Before opening a PR against an external repo:
1. Read the entire PR template and fill in every section with real, specific answers
2. Search for existing PRs — open AND closed — that address the same problem
3. Verify this is a real problem someone actually experienced
4. Confirm the change belongs in core, not a standalone plugin/extension
5. Show the complete diff and get explicit approval before submitting

One problem per PR. Bundled unrelated changes will be rejected.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, clarifying questions come before implementation rather than after mistakes, and verification passes before reporting success.
