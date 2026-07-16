#!/bin/bash
# ==============================================================
# shutdown.sh — Desliga o PC host remotamente via SSH
# Coloque este arquivo em: /DATA/AppData/wake-on-lan/shutdown.sh
# ==============================================================

# ─── Configuração ───────────────────────────────────────────
TARGET_HOST="<IP_DO_SEU_SERVIDOR>"   # IP do PC a desligar
TARGET_USER="<usuario_SSH>"          # usuário SSH do PC alvo
SSH_KEY="/scripts/id_rsa"      # chave privada SSH (montar via volume)
SSH_PORT=22                    # porta SSH (padrão 22)
# ────────────────────────────────────────────────────────────

set -euo pipefail

echo "[shutdown] Enviando comando de desligamento para ${TARGET_USER}@${TARGET_HOST}..."

ssh \
  -i "$SSH_KEY" \
  -o StrictHostKeyChecking=no \
  -o ConnectTimeout=8 \
  -p "$SSH_PORT" \
  "${TARGET_USER}@${TARGET_HOST}" \
  "shutdown /s /t 0"

echo "[shutdown] Comando enviado com sucesso."
