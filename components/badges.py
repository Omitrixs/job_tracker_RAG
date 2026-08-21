def render_badge(status):
    status_lower = status.lower()
    return f'<span class="badge badge-{status_lower}">{status.upper()}</span>'