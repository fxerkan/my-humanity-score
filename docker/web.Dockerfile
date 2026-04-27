FROM node:20-alpine AS base

WORKDIR /app

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# ── deps stage ────────────────────────────────────────────────────────────────
FROM base AS deps
COPY apps/web/package.json apps/web/pnpm-lock.yaml* ./
RUN pnpm install --frozen-lockfile 2>/dev/null || pnpm install

# ── dev stage (used by docker-compose) ───────────────────────────────────────
FROM base AS dev
COPY --from=deps /app/node_modules ./node_modules
COPY apps/web/ .
EXPOSE 3000
CMD ["pnpm", "dev"]

# ── builder stage ─────────────────────────────────────────────────────────────
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY apps/web/ .
RUN pnpm build

# ── production stage ──────────────────────────────────────────────────────────
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
