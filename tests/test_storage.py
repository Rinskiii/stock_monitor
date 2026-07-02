from monitor.storage import load_alerts, save_alerts

print("=== Первая загрузка ===")
alerts = load_alerts()
print(alerts)

print("\n=== Сохраняем ===")
alerts = {"RKLB", "PLTR", "CRDO"}
save_alerts(alerts)

print("\n=== Повторная загрузка ===")
alerts = load_alerts()
print(alerts)