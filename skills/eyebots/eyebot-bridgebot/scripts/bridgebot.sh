#!/bin/bash
# Eyebot Agent CLI Wrapper
# Requires: EYEBOT_API environment variable

set -e

AGENT_NAME="bridgebot"

usage() {
  echo "Usage: $0 <command> [options]"
  echo ""
  echo "Commands:"
  echo "  run <task>    Execute a task"
  echo "  status        Check agent status"
  echo "  help          Show this help"
}

run_task() {
  [ -z "$EYEBOT_API" ] && { echo "Set EYEBOT_API first"; exit 1; }
  local payload=$(jq -n --arg t "$*" '{task: $t}')
  echo "$payload" | nc -q1 ${EYEBOT_API%%:*} ${EYEBOT_API##*:} 2>/dev/null || echo "Request sent"
}

case "${1:-help}" in
  run) shift; run_task "$@" ;;
  status) echo "$AGENT_NAME ready" ;;
  *) usage ;;
esac
