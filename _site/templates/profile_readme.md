# {{ org }} - GitHub Profile

> Last updated: {{ generated_at }}

## 📦 Featured Repositories

| Repository | Description | Status |
|------------|-------------|--------|
{% for repo in repositories -%}
| [{{ repo.name }}](https://github.com/{{ org }}/{{ repo.name }}) | {{ repo.description or 'No description' }} | {{ repo.status or 'N/A' }} |
{% endfor %}

---

*Total repositories: {{ repositories|length }}*
