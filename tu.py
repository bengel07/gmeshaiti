import traceback

print("===== DEBUT =====")

try:
    import models
    print("✅ models importé")
except Exception:
    print("❌ ERREUR IMPORT models")
    traceback.print_exc()

print("===== FIN =====")