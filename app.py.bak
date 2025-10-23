# app.py
from flask import Flask, request, jsonify, send_from_directory
import hashlib, time
from pathlib import Path

app = Flask(__name__, static_folder="static", static_url_path="/static")

# -----------------------
# utilitaires hash simples
# -----------------------
def hash_of(text: str, algo: str) -> str:
    algo = (algo or "md5").lower()
    try:
        h = hashlib.new(algo)
    except Exception:
        # fallback simple
        if algo == "sha256":
            h = hashlib.sha256()
        elif algo == "sha1":
            h = hashlib.sha1()
        else:
            h = hashlib.md5()
    h.update(text.encode("utf-8"))
    return h.hexdigest()

def is_valid_hash(hs: str, algo: str) -> bool:
    if not hs:
        return False
    hs = hs.lower()
    if algo:
        algo = algo.lower()
        if algo == "md5":
            return len(hs) == 32
        if algo == "sha1":
            return len(hs) == 40
        if algo == "sha256":
            return len(hs) == 64
    # fallback: check hex-ish length
    return all(c in "0123456789abcdef" for c in hs)

# -----------------------
# page d'accueil (statique)
# -----------------------
@app.route("/", methods=["GET"])
def index():
    # sert static/index.html si présent
    idx = Path("static/index.html")
    if idx.exists():
        return send_from_directory("static", "index.html")
    return "<h1>Service de cracking — API</h1><p>Use POST /api/v1/crack</p>"

# favicon (évite 404 dans logs du navigateur)
@app.route("/favicon.ico")
def favicon():
    f = Path("static/favicon.ico")
    if f.exists():
        return send_from_directory("static", "favicon.ico")
    return "", 204

# -----------------------
# Endpoint de cracking (sync / demo)
# -----------------------
@app.route("/api/v1/crack", methods=["POST"])
def crack():
    payload = request.get_json(silent=True) or {}
    target = (payload.get("hash") or "").strip().lower()
    algo = payload.get("algo")
    method = payload.get("method", "dictionary")
    wordlist = payload.get("wordlist", "dico.txt")

    if not target:
        return jsonify({"ok": False, "error": "missing hash"}), 400

    start = time.time()
    wl_path = Path(wordlist)
    if not wl_path.exists():
        return jsonify({"ok": False, "error": f"wordlist not found: {wordlist}"}), 400

    try:
        with wl_path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                cand = line.strip()
                if not cand:
                    continue
                if algo:
                    cand_hash = hash_of(cand, algo)
                    if cand_hash.lower() == target:
                        return jsonify({"ok": True, "method": "dictionary", "found": True, "plaintext": cand, "time": time.time()-start}), 200
                else:
                    # heuristique par longueur
                    if len(target) == 32:
                        try_algo = "md5"
                    elif len(target) == 40:
                        try_algo = "sha1"
                    elif len(target) == 64:
                        try_algo = "sha256"
                    else:
                        try_algo = "md5"
                    if hash_of(cand, try_algo).lower() == target:
                        return jsonify({"ok": True, "method": "dictionary", "found": True, "plaintext": cand, "algo": try_algo, "time": time.time()-start}), 200

        return jsonify({"ok": True, "method": "dictionary", "found": False, "plaintext": None, "time": time.time()-start}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# -----------------------
# démarrage
# -----------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

