from flask import Flask, jsonify, render_template
import subprocess
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MAC_ADDRESS = os.environ.get("WOL_MAC", "D8:43:AE:B2:80:C7")

# Caminho do script dentro do container (montado via volume no docker-compose)
SCRIPT_PATH        = "/scripts/wake_on_lan.sh"
SHUTDOWN_SCRIPT    = "/scripts/shutdown.sh"

@app.route("/")
def index():
    return render_template("index.html", mac=MAC_ADDRESS)

@app.route("/wake", methods=["POST"])
def wake():
    try:
        if not os.path.isfile(SCRIPT_PATH):
            return jsonify({"status": "error", "message": f"Script não encontrado: {SCRIPT_PATH}"}), 500

        result = subprocess.run(
            ["/bin/bash", SCRIPT_PATH],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            app.logger.info(f"Script executado com sucesso: {SCRIPT_PATH}")
            return jsonify({"status": "success", "message": "Pacote mágico enviado! ✓"})
        else:
            app.logger.error(f"Erro no script: {result.stderr}")
            return jsonify({"status": "error", "message": result.stderr or "Erro ao executar script"}), 500
    except Exception as e:
        app.logger.exception("Erro ao executar wake_on_lan.sh")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/shutdown", methods=["POST"])
def shutdown():
    try:
        if not os.path.isfile(SHUTDOWN_SCRIPT):
            return jsonify({"status": "error", "message": f"Script não encontrado: {SHUTDOWN_SCRIPT}"}), 500

        result = subprocess.run(
            ["/bin/bash", SHUTDOWN_SCRIPT],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0:
            app.logger.info(f"Script de desligamento executado: {SHUTDOWN_SCRIPT}")
            return jsonify({"status": "success", "message": "Comando de desligamento enviado! ✓"})
        else:
            app.logger.error(f"Erro no script de desligamento: {result.stderr}")
            return jsonify({"status": "error", "message": result.stderr or "Erro ao executar script de desligamento"}), 500
    except Exception as e:
        app.logger.exception("Erro ao executar shutdown.sh")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
