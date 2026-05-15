#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s <read|write|execute|auth|user> <RequestType> [params_json]\n' "$0" >&2
}

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
  usage
  exit 2
fi

path="$1"
request_type="$2"
params_json="${3:-{}}"

case "$path" in
  read|write|execute|auth|user) ;;
  *)
    printf 'Invalid path: %s\n' "$path" >&2
    usage
    exit 2
    ;;
esac

base_url="${KOMODO_URL:-}"
api_key="${KOMODO_API_KEY:-}"
api_secret="${KOMODO_API_SECRET:-}"

if [ -z "$base_url" ]; then
  printf 'Missing KOMODO_URL environment variable\n' >&2
  exit 1
fi

if [ -z "$api_key" ]; then
  printf 'Missing KOMODO_API_KEY environment variable\n' >&2
  exit 1
fi

if [ -z "$api_secret" ]; then
  printf 'Missing KOMODO_API_SECRET environment variable\n' >&2
  exit 1
fi

if ! jq -e . >/dev/null 2>&1 <<<"$params_json"; then
  printf 'params_json must be valid JSON\n' >&2
  exit 2
fi

base_url="${base_url%/}"

curl --fail-with-body --silent --show-error \
  --request POST \
  --header 'Content-Type: application/json' \
  --header "X-Api-Key: $api_key" \
  --header "X-Api-Secret: $api_secret" \
  --data "$params_json" \
  "$base_url/$path/$request_type"
