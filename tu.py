from app import app

def afficher_endpoints():
    print("\n" + "=" * 100)
    print(f"{'ENDPOINT':40} {'METHODS':20} URL")
    print("=" * 100)

    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        methods = ", ".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
        print(f"{rule.endpoint:40} {methods:20} {rule.rule}")

    print("=" * 100)
    print(f"Total des endpoints : {len(app.url_map._rules)}")

if __name__ == "__main__":
    afficher_endpoints()