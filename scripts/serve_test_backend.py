#!/usr/bin/env python3
"""Serve a local authenticated admin fixture for browser-skill testing.

Routes
- /login                login form (admin / demo-pass)
- /admin                authenticated dashboard with filters and pagination
- /detail?id=...        authenticated detail page
- /upload               authenticated file upload handler
- /export.csv           authenticated CSV export
"""

from __future__ import annotations

import argparse
import csv
import html
import io
import re
import secrets
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

RECORDS = [
    {"id": "ORD-1001", "title": "Browser audit", "status": "open", "owner": "alice", "kind": "browser"},
    {"id": "ORD-1002", "title": "Agent rollout", "status": "open", "owner": "bob", "kind": "agent"},
    {"id": "ORD-1003", "title": "Legacy cleanup", "status": "closed", "owner": "cara", "kind": "ops"},
    {"id": "ORD-1004", "title": "Browser export", "status": "open", "owner": "dave", "kind": "browser"},
    {"id": "ORD-1005", "title": "Agent import", "status": "queued", "owner": "erin", "kind": "agent"},
    {"id": "ORD-1006", "title": "Ops checklist", "status": "closed", "owner": "frank", "kind": "ops"},
]
SESSIONS: dict[str, dict] = {}
PAGE_SIZE = 2


def page(title: str, body: str) -> bytes:
    return f"""<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\">
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 920px; margin: 2rem auto; line-height: 1.4; }}
    label, input, select, button {{ font-size: 16px; }}
    .card {{ border: 1px solid #ddd; border-radius: 10px; padding: 1rem; margin: 1rem 0; }}
    .meta {{ color: #555; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
    th, td {{ border: 1px solid #ddd; padding: .6rem; text-align: left; }}
    .toolbar {{ display: flex; gap: 12px; flex-wrap: wrap; align-items: end; }}
    .notice {{ background: #eef7ff; border: 1px solid #b6d9ff; padding: .8rem; border-radius: 8px; }}
  </style>
</head>
<body>
{body}
</body>
</html>
""".encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    server_version = "UBSFixture/2.0"

    def log_message(self, fmt: str, *args) -> None:
        return

    def get_session(self):
        raw = self.headers.get("Cookie")
        if not raw:
            return None
        cookie = SimpleCookie()
        cookie.load(raw)
        sid = cookie.get("sid")
        if not sid:
            return None
        return SESSIONS.get(sid.value)

    def require_session(self):
        session = self.get_session()
        if session:
            return session
        next_url = urlparse(self.path).path
        if urlparse(self.path).query:
            next_url += "?" + urlparse(self.path).query
        self.send_response(HTTPStatus.FOUND)
        self.send_header("Location", f"/login?next={html.escape(next_url, quote=True)}")
        self.end_headers()
        return None

    def send_html(self, title: str, body: str, status: int = 200, headers: dict[str, str] | None = None):
        payload = page(title, body)
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        if headers:
            for k, v in headers.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        parsed = urlparse(self.path)
        route = parsed.path
        if route == "/":
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Location", "/admin")
            self.end_headers()
            return
        if route == "/login":
            return self.render_login()
        if route == "/admin":
            return self.render_admin(parsed)
        if route == "/detail":
            return self.render_detail(parsed)
        if route == "/export.csv":
            return self.render_export(parsed)
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/login":
            return self.handle_login()
        if parsed.path == "/upload":
            return self.handle_upload()
        self.send_error(HTTPStatus.NOT_FOUND)

    def render_login(self):
        parsed = urlparse(self.path)
        next_url = parse_qs(parsed.query).get("next", ["/admin"])[0]
        self.send_html(
            "UBS Login",
            f"""
            <h1>UBS Admin Login</h1>
            <p class=\"meta\">Use username <strong>admin</strong> and password <strong>demo-pass</strong>.</p>
            <form method=\"post\" action=\"/login\" class=\"card\">
              <input type=\"hidden\" name=\"next\" value=\"{html.escape(next_url, quote=True)}\">
              <p><label>Username <input aria-label=\"Username\" name=\"username\"></label></p>
              <p><label>Password <input aria-label=\"Password\" name=\"password\" type=\"password\"></label></p>
              <p><label>Workspace
                <select aria-label=\"Workspace\" name=\"workspace\">
                  <option value=\"alpha\">alpha</option>
                  <option value=\"beta\">beta</option>
                </select>
              </label></p>
              <button type=\"submit\">Sign in</button>
            </form>
            """,
        )

    def handle_login(self):
        length = int(self.headers.get("Content-Length", "0"))
        data = parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True)
        username = data.get("username", [""])[0]
        password = data.get("password", [""])[0]
        workspace = data.get("workspace", ["alpha"])[0]
        next_url = data.get("next", ["/admin"])[0]
        if username == "admin" and password == "demo-pass":
            sid = secrets.token_hex(16)
            SESSIONS[sid] = {"username": username, "workspace": workspace, "last_upload": None}
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Set-Cookie", f"sid={sid}; HttpOnly; Path=/; SameSite=Lax")
            self.send_header("Location", next_url)
            self.end_headers()
            return
        self.send_html("Login failed", "<h1>Login failed</h1><p>Invalid credentials.</p>", status=401)

    def filtered_records(self, parsed):
        params = parse_qs(parsed.query)
        q = params.get("q", [""])[0].strip().lower()
        status = params.get("status", ["all"])[0]
        page_num = max(1, int(params.get("page", ["1"])[0]))
        rows = RECORDS
        if status != "all":
            rows = [r for r in rows if r["status"] == status]
        if q:
            rows = [r for r in rows if q in r["id"].lower() or q in r["title"].lower() or q in r["owner"].lower()]
        return params, rows, page_num

    def render_admin(self, parsed):
        session = self.require_session()
        if not session:
            return
        params, rows, page_num = self.filtered_records(parsed)
        start = (page_num - 1) * PAGE_SIZE
        page_rows = rows[start : start + PAGE_SIZE]
        next_link = ""
        if start + PAGE_SIZE < len(rows):
            query = dict((k, v[0]) for k, v in params.items())
            query["page"] = str(page_num + 1)
            next_link = f'<a id="next-page" href="/admin?{urlencode(query)}">Next page</a>'
        upload_note = ""
        if session.get("last_upload"):
            upload_note = f"<p class='notice'>Last upload: {html.escape(session['last_upload'])}</p>"
        rows_html = "".join(
            f"<tr><td><a href='/detail?id={r['id']}'>{html.escape(r['id'])}</a></td><td>{html.escape(r['title'])}</td><td>{html.escape(r['status'])}</td><td>{html.escape(r['owner'])}</td></tr>"
            for r in page_rows
        ) or "<tr><td colspan='4'>No records</td></tr>"
        self.send_html(
            "UBS Admin Dashboard",
            f"""
            <h1>UBS Admin Dashboard</h1>
            <p class=\"meta\">Signed in as <strong>{html.escape(session['username'])}</strong> in workspace <strong>{html.escape(session['workspace'])}</strong>.</p>
            <div class=\"card\">
              <form method=\"get\" action=\"/admin\">
                <div class=\"toolbar\">
                  <p><label>Search <input aria-label=\"Search\" name=\"q\" value=\"{html.escape(params.get('q', [''])[0])}\"></label></p>
                  <p><label>Status
                    <select aria-label=\"Status\" name=\"status\">
                      <option value=\"all\" {'selected' if params.get('status', ['all'])[0] == 'all' else ''}>all</option>
                      <option value=\"open\" {'selected' if params.get('status', ['all'])[0] == 'open' else ''}>open</option>
                      <option value=\"queued\" {'selected' if params.get('status', ['all'])[0] == 'queued' else ''}>queued</option>
                      <option value=\"closed\" {'selected' if params.get('status', ['all'])[0] == 'closed' else ''}>closed</option>
                    </select>
                  </label></p>
                  <button type=\"submit\">Apply filters</button>
                  <a id=\"export-link\" href=\"/export.csv?{urlencode({k: v[0] for k, v in params.items() if v and k != 'page'})}\">Export CSV</a>
                </div>
              </form>
            </div>
            <p id=\"result-summary\">{len(rows)} matching records | page {page_num}</p>
            <table>
              <thead><tr><th>ID</th><th>Title</th><th>Status</th><th>Owner</th></tr></thead>
              <tbody>{rows_html}</tbody>
            </table>
            <p>{next_link or 'No more pages'}</p>
            <div class=\"card\">
              <h2>Imports</h2>
              {upload_note}
              <form method=\"post\" action=\"/upload\" enctype=\"multipart/form-data\">
                <p><label>Import file <input aria-label=\"Import file\" name=\"upload\" type=\"file\"></label></p>
                <button type=\"submit\">Upload import</button>
              </form>
            </div>
            """,
        )

    def render_detail(self, parsed):
        session = self.require_session()
        if not session:
            return
        record_id = parse_qs(parsed.query).get("id", [""])[0]
        row = next((r for r in RECORDS if r["id"] == record_id), None)
        if not row:
            return self.send_html("Missing record", "<h1>Record not found</h1>", status=404)
        self.send_html(
            f"Detail {record_id}",
            f"""
            <h1>Detail for {html.escape(row['id'])}</h1>
            <p id=\"detail-meta\">title={html.escape(row['title'])} | status={html.escape(row['status'])} | workspace={html.escape(session['workspace'])}</p>
            <p><a id=\"back-to-admin\" href=\"/admin\">Back to dashboard</a></p>
            <p><a id=\"download-report\" href=\"/export.csv?record={html.escape(row['id'])}\">Download report</a></p>
            """,
        )

    def handle_upload(self):
        session = self.require_session()
        if not session:
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        filename = None
        match = re.search(br'filename="([^\"\r\n]+)"', raw)
        if match:
            filename = match.group(1).decode("utf-8", errors="replace")
        if filename:
            session["last_upload"] = filename
        self.send_response(HTTPStatus.FOUND)
        self.send_header("Location", "/admin")
        self.end_headers()

    def render_export(self, parsed):
        session = self.require_session()
        if not session:
            return
        params = parse_qs(parsed.query)
        record = params.get("record", [None])[0]
        rows = RECORDS
        if record:
            rows = [r for r in rows if r["id"] == record]
        else:
            _, rows, _ = self.filtered_records(parsed)
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=["id", "title", "status", "owner", "kind"])
        writer.writeheader()
        writer.writerows(rows)
        data = buffer.getvalue().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/csv; charset=utf-8")
        self.send_header("Content-Disposition", "attachment; filename=ubs-export.csv")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve a local authenticated admin test backend.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8124)
    args = parser.parse_args()

    with ThreadingHTTPServer((args.host, args.port), Handler) as httpd:
        print(f"UBS test backend listening on http://{args.host}:{args.port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
