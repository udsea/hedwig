#!/bin/bash

echo "⚛️ Starting Hedwig Frontend..."
cd frontend

# Install dependencies and start
if command -v bun >/dev/null 2>&1; then
    echo "Using Bun..."
    bun install
    bun run dev
else
    echo "Using npm..."
    npm install
    npm run dev
fi
