#!/usr/bin/env bash
# Restore Postgres from a dump produced by the db-backup sidecar.
# See deploy/RESTORE.md for the full runbook.
#
# Usage:
#   ./deploy/restore.sh                                          # latest
#   ./deploy/restore.sh /backups/daily/mairie-2026-05-05.sql.gz  # specific
#
# Run from the repo root on the prod host.

set -euo pipefail

# ─── Locate the repo root and load env ────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"

if [[ ! -f .env.prod ]]; then
    echo "ERROR: .env.prod not found in $ROOT" >&2
    exit 1
fi
# Load POSTGRES_DB so the default dump path resolves correctly
set -a; source .env.prod; set +a

DUMP="${1:-/backups/last/${POSTGRES_DB}-latest.sql.gz}"
COMPOSE=(docker compose --env-file .env.prod
    -f docker-compose.yml -f docker-compose.prod.yml)

# ─── Sanity checks ────────────────────────────────────────────────────────
if ! "${COMPOSE[@]}" ps db-backup --status running | grep -q db-backup; then
    echo "ERROR: db-backup service is not running. Start the stack first." >&2
    exit 1
fi

if ! "${COMPOSE[@]}" exec -T db-backup test -f "$DUMP"; then
    echo "ERROR: dump not found inside the db-backup container at $DUMP" >&2
    echo "Available:" >&2
    "${COMPOSE[@]}" exec -T db-backup find /backups -name '*.sql.gz' -printf '  %p\n' | sort >&2
    exit 1
fi

DUMP_SIZE=$("${COMPOSE[@]}" exec -T db-backup stat -c '%s' "$DUMP")
echo "About to restore database '${POSTGRES_DB}' from:"
echo "  $DUMP  (${DUMP_SIZE} bytes)"
echo "This will REPLACE every row currently in the database."
read -rp "Type RESTORE in capitals to confirm: " CONFIRM
if [[ "$CONFIRM" != "RESTORE" ]]; then
    echo "Aborted." >&2
    exit 1
fi

# ─── 1. Pause writers ─────────────────────────────────────────────────────
echo
echo "→ Stopping backend (pauses all writers)…"
"${COMPOSE[@]}" stop backend

# ─── 2. Panic dump of current state ───────────────────────────────────────
echo "→ Taking a safety dump of the current state (in case the restore fails)…"
"${COMPOSE[@]}" exec -T db-backup /backup.sh
echo "  Latest pre-restore dump:"
"${COMPOSE[@]}" exec -T db-backup ls -lh /backups/last/

# ─── 3. Restore ───────────────────────────────────────────────────────────
echo "→ Restoring from $DUMP …"
"${COMPOSE[@]}" exec -T db-backup /restore.sh "$DUMP"

# ─── 4. Restart writers ───────────────────────────────────────────────────
echo "→ Starting backend back up…"
"${COMPOSE[@]}" start backend

echo
echo "✅ Restore complete."
echo "   Tail the backend logs to confirm a clean start:"
echo "     ${COMPOSE[*]} logs -f backend"
