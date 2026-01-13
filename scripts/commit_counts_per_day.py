import requests
import datetime
import os
from collections import Counter
import matplotlib.pyplot as plt

USERNAME = "bsubhamay"
GITHUB_API = "https://api.github.com"
token = os.getenv("GITHUB_TOKEN")

headers = {"Authorization": f"token {token}"}
events = requests.get(
    f"{GITHUB_API}/users/{USERNAME}/events",
    headers=headers
).json()

dates = []
for e in events:
    if e["type"] == "PushEvent":
        date = e["created_at"][:10]
        dates.append(date)

counts = Counter(dates)
days = sorted(counts)
values = [counts[d] for d in days]

plt.figure()
plt.plot(days, values)
plt.xticks(rotation=45)
plt.title("Daily GitHub Commits")
plt.tight_layout()
plt.savefig("commits-per-day.svg")
