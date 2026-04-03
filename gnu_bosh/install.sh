#!/usr/bin/env bash

# Should run like ```REMOTE_USER=john REMOTE_PASS=mypassword ./install.sh```

set -euo pipefail

# config
REMOTE_USER="${REMOTE_USER:-admin}"
REMOTE_PASS="${REMOTE_PASS:-}"                                 # Set via env var or prompt
REMOTE_HOSTS=("100.65.3.116")   # Edit as needed
SOURCE_DIR="${SOURCE_DIR:-./gnu_bash}"        # Local path to source files
REMOTE_TMP="${REMOTE_TMP:-/tmp/systemd-build}"  # Staging dir on remote machines
INSTALL_PREFIX="${INSTALL_PREFIX:-/usr}"


log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
die() { echo "[ERROR] $*" >&2; exit 1; }

check_deps() {
  if ! command -v sshpass &>/dev/null; then
    log "sshpass not found — installing..."
    sudo apt-get update -qq && sudo apt-get install -y sshpass \
      || die "Failed to install sshpass. Run: sudo apt-get install sshpass"
  fi
  for cmd in ssh scp; do
    command -v "$cmd" &>/dev/null || die "'$cmd' not found in PATH."
  done
}

prompt_password() {
  if [[ -z "${REMOTE_PASS}" ]]; then
    read -rsp "Enter SSH password for '${REMOTE_USER}': " REMOTE_PASS
    echo ""
    [[ -n "${REMOTE_PASS}" ]] || die "Password cannot be empty."
  fi
}

sp_ssh() {
  sshpass -p "${REMOTE_PASS}" ssh \
    -o StrictHostKeyChecking=no \
    -o ConnectTimeout=10 \
    "$@"
}

sp_scp() {
  sshpass -p "${REMOTE_PASS}" scp \
    -o StrictHostKeyChecking=no \
    -o ConnectTimeout=10 \
    "$@"
}

deploy_to_host() {
  local host="$1"
  log "═══ Deploying to ${REMOTE_USER}@${host} ═══"

  log "[${host}] Installing build dependencies..."
  sp_ssh "${REMOTE_USER}@${host}" \
    "echo "${REMOTE_PASS}" | sudo -S DEBIAN_FRONTEND=noninteractive apt-get update"
  sp_ssh "${REMOTE_USER}@${host}" \
    "echo "${REMOTE_PASS}" | sudo -S DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential gcc autoconf"

  log "[${host}] Creating remote staging directory: ${REMOTE_TMP}"
  sp_ssh "${REMOTE_USER}@${host}" "mkdir '${REMOTE_TMP}'"

  log "[${host}] Transferring source files..."
  sp_scp -r "${SOURCE_DIR}/." "${REMOTE_USER}@${host}:${REMOTE_TMP}/"

  # run configure and build
  log "[${host}] Running configure, make, and install..."
  sp_ssh "${REMOTE_USER}@${host}" bash <<EOF
    set -euo pipefail
    cd '${REMOTE_TMP}'

    echo "--- Running configure ---"
    echo "${REMOTE_PASS}" | sudo -s -S
    sh ./configure
    make install

    echo "--- Verifying installation ---"
    '${INSTALL_PREFIX}/bin/bash' --version

    echo "--- Cleaning up staging directory ---"
    rm -rf '${REMOTE_TMP}'
EOF

  log "[${host}]: Deployment complete."
}

main() {
  check_deps
  prompt_password

  [[ -d "${SOURCE_DIR}" ]] || die "Source directory '${SOURCE_DIR}' not found."
  [[ ${#REMOTE_HOSTS[@]} -gt 0 ]] || die "No remote hosts defined."

  local failed=()

  for host in "${REMOTE_HOSTS[@]}"; do
    if deploy_to_host "$host"; then
      log "✓ ${host} succeeded."
    else
      log "✗ ${host} failed — continuing to next host."
      failed+=("$host")
    fi
  done

  if [[ ${#failed[@]} -gt 0 ]]; then
    echo ""
    log "Deployment finished with failures on: ${failed[*]}"
    exit 1
  else
    log "All hosts deployed successfully."
  fi
}

main "$@"