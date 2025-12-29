---
slug: operational-rules
description: Defines standard operational commands and procedures.
trigger: model_decision
---
# Operational Standards

## Build & Test
- **Build Command**: pnpm run build (or 
pm run build in contexts where pnpm is not available)
- **Test Command**: 
ode --test (native Node.js test runner) or 
pm test`r
- **Install Command**: pnpm install`r

## Version Control
- **Commits**: Use semantically meaningful messages (Japanese preferred for descriptions).
- **Branching**: Follow Git Flow (develop, feature/xxx, main).
