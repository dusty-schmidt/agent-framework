#!/usr/bin/env bash
set -euo pipefail

# [GOB] :: Config
API_KEY="${GEMINI_API_KEY}"
MODEL_ENDPOINT="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
LOG_FILE="/root/gemini_pinger.log"
TMP_REQ="/root/gemini_request.json"
TMP_RESP="/root/gemini_response.json"

# [GOB] :: Guardrails
if [[ -z "${API_KEY}" ]]; then
  echo "[$(date -Is)] ERROR: GEMINI_API_KEY not set in environment" | tee -a "$LOG_FILE"
  exit 1
fi

# [GOB] :: Prompt pool for randomization
PROMPTS=(
  "Explain how AI works in a few words"
  "Summarize quantum computing in one sentence"
  "Give a fun fact about space in fewer than 10 words"
  "Describe recursion tersely"
  "What is the capital of France?"
  "Offer a productivity tip in one short line"
  "State a haiku about code"
  "Explain HTTP in a single sentence"
)

# [GOB] :: Pick a random prompt
RANDOM_PROMPT=${PROMPTS[$RANDOM % ${#PROMPTS[@]}]}

# [GOB] :: Build request JSON safely
cat >"$TMP_REQ" <<REQ
{
  "contents": [
    {
      "parts": [
        { "text": "${RANDOM_PROMPT//"/\\\"}" }
      ]
    }
  ]
}
REQ

# [GOB] :: Execute request
HTTP_CODE=$(curl -sS -w "%{http_code}" \
  -H 'Content-Type: application/json' \
  -H "X-goog-api-key: ${API_KEY}" \
  -X POST \
  -d @"$TMP_REQ" \
  "$MODEL_ENDPOINT" \
  -o "$TMP_RESP" || true)

# [GOB] :: Log results with timestamp
{
  echo "==== $(date -Is) ===="
  echo "Prompt: $RANDOM_PROMPT"
  echo "HTTP: $HTTP_CODE"
  if command -v jq >/dev/null 2>&1; then
    echo "Response:"
    jq '.' "$TMP_RESP" || cat "$TMP_RESP"
  else
    echo "Response (raw):"
    cat "$TMP_RESP"
  fi
  echo
} >>"$LOG_FILE"

# [GOB] :: Optional: basic failure signaling
if [[ "$HTTP_CODE" -lt 200 || "$HTTP_CODE" -ge 300 ]]; then
  exit 2
fi
