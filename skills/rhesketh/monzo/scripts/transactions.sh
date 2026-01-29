#!/bin/bash
# View, search, and annotate Monzo transactions
# Usage: transactions [options] [account-id]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/monzo.sh"

# Parse arguments
OUTPUT_MODE="human"
ARG_ACCOUNT_ID=""
SINCE=""
BEFORE=""
LIMIT="100"
SEARCH_TERM=""
TRANSACTION_ID=""
ANNOTATE_KEY=""
ANNOTATE_VALUE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --since)
      SINCE=$(monzo_parse_date "$2")
      shift 2
      ;;
    --before)
      BEFORE=$(monzo_parse_date "$2")
      shift 2
      ;;
    --limit)
      LIMIT="$2"
      shift 2
      ;;
    --search)
      SEARCH_TERM="$2"
      shift 2
      ;;
    --id)
      TRANSACTION_ID="$2"
      shift 2
      ;;
    --annotate)
      if [[ "$2" =~ ^([^=]+)=(.*)$ ]]; then
        ANNOTATE_KEY="${BASH_REMATCH[1]}"
        ANNOTATE_VALUE="${BASH_REMATCH[2]}"
      else
        echo "Error: --annotate format should be KEY=VALUE" >&2
        exit 1
      fi
      shift 2
      ;;
    --json)
      OUTPUT_MODE="json"
      shift
      ;;
    -h|--help)
      echo "Usage: transactions [options] [account-id]"
      echo ""
      echo "View, search, and annotate transactions"
      echo ""
      echo "Arguments:"
      echo "  account-id          Account ID (uses default if not specified)"
      echo ""
      echo "Options:"
      echo "  --since DATE        Start date (ISO 8601, YYYY-MM-DD, or '7d' for relative)"
      echo "  --before DATE       End date (ISO 8601 or YYYY-MM-DD)"
      echo "  --limit N           Max transactions to return (default: 100)"
      echo "  --search TERM       Filter by description/merchant (client-side)"
      echo "  --id TX_ID          Get specific transaction"
      echo "  --annotate KEY=VAL  Add metadata to transaction (requires --id)"
      echo "  --json              Output raw JSON response"
      echo "  -h, --help          Show this help message"
      echo ""
      echo "Examples:"
      echo "  transactions --limit 10"
      echo "  transactions --since 7d"
      echo "  transactions --search coffee --since 30d"
      echo "  transactions --id tx_... --annotate category=groceries"
      exit 0
      ;;
    acc_*)
      ARG_ACCOUNT_ID="$1"
      shift
      ;;
    *)
      echo "Error: Unknown option: $1" >&2
      echo "Use --help for usage information" >&2
      exit 1
      ;;
  esac
done

# Load credentials
monzo_load_credentials

# Handle annotation
if [[ -n "$ANNOTATE_KEY" ]]; then
  if [[ -z "$TRANSACTION_ID" ]]; then
    echo "Error: --annotate requires --id to specify which transaction" >&2
    exit 1
  fi

  # Annotate the transaction
  response=$(monzo_api_call PATCH "/transactions/$TRANSACTION_ID" \
    -d "metadata[$ANNOTATE_KEY]=$ANNOTATE_VALUE")

  if [[ "$OUTPUT_MODE" == "json" ]]; then
    echo "$response"
  else
    echo "✓ Transaction annotated: $ANNOTATE_KEY = $ANNOTATE_VALUE"
  fi
  exit 0
fi

# Handle single transaction lookup
if [[ -n "$TRANSACTION_ID" ]]; then
  response=$(monzo_api_call GET "/transactions/$TRANSACTION_ID?expand[]=merchant")

  if [[ "$OUTPUT_MODE" == "json" ]]; then
    echo "$response"
    exit 0
  fi

  # Human-readable single transaction
  tx=$(jq -r '.transaction' <<< "$response")
  created=$(jq -r '.created' <<< "$tx")
  amount=$(jq -r '.amount' <<< "$tx")
  currency=$(jq -r '.currency' <<< "$tx")
  description=$(jq -r '.description' <<< "$tx")
  merchant_name=$(jq -r '.merchant.name // "N/A"' <<< "$tx")
  category=$(jq -r '.category' <<< "$tx")
  notes=$(jq -r '.notes // ""' <<< "$tx")

  echo "Transaction: $TRANSACTION_ID"
  echo "Date: $(monzo_format_date "$created")"
  echo "Amount: $(monzo_format_money "$amount" "$currency")"
  echo "Description: $description"
  echo "Merchant: $merchant_name"
  echo "Category: $category"
  if [[ -n "$notes" ]]; then
    echo "Notes: $notes"
  fi

  # Show metadata if any
  metadata=$(jq -r '.metadata // {}' <<< "$tx")
  if [[ "$metadata" != "{}" ]]; then
    echo ""
    echo "Metadata:"
    jq -r 'to_entries[] | "  \(.key): \(.value)"' <<< "$metadata"
  fi

  exit 0
fi

# Get account ID
ACCOUNT_ID=$(monzo_ensure_account_id "$ARG_ACCOUNT_ID") || exit 1

# Build query parameters
QUERY="account_id=$ACCOUNT_ID&limit=$LIMIT"

if [[ -n "$SINCE" ]]; then
  QUERY="$QUERY&since=$SINCE"
fi

if [[ -n "$BEFORE" ]]; then
  QUERY="$QUERY&before=$BEFORE"
fi

# Fetch transactions
response=$(monzo_api_call GET "/transactions?$QUERY&expand[]=merchant")

# JSON mode - output raw response
if [[ "$OUTPUT_MODE" == "json" ]]; then
  echo "$response"
  exit 0
fi

# Human-readable mode
transactions=$(jq -r '.transactions' <<< "$response")

# Apply client-side search filter if specified
if [[ -n "$SEARCH_TERM" ]]; then
  transactions=$(jq --arg term "$SEARCH_TERM" \
    '[.[] | select(.description | ascii_downcase | contains($term | ascii_downcase)) or (.merchant.name // "" | ascii_downcase | contains($term | ascii_downcase))]' \
    <<< "$transactions")
fi

# Count transactions
count=$(jq 'length' <<< "$transactions")

if [[ "$count" == "0" ]]; then
  echo "No transactions found"
  exit 0
fi

# Display transactions in table format
printf "%-12s %-10s %-35s %-15s\n" "DATE" "AMOUNT" "DESCRIPTION" "CATEGORY"
printf "%-12s %-10s %-35s %-15s\n" "============" "==========" "===================================" "==============="

jq -r '.[] |
  [
    (.created | split("T")[0]),
    (.amount | tostring),
    (.currency),
    (.description[0:35]),
    (.category // "uncategorized")
  ] | @tsv' <<< "$transactions" | \
while IFS=$'\t' read -r date amount currency description category; do
  formatted_amount=$(monzo_format_money "$amount" "$currency")
  printf "%-12s %-10s %-35s %-15s\n" "$date" "$formatted_amount" "$description" "$category"
done

echo ""
echo "Total: $count transaction(s)"
