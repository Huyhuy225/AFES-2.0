"""Minimal read-only HTTP health/status endpoint for Local Gateway operations."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Callable

from .gateway import LocalGateway


def make_handler(snapshot_fn: Callable[[], dict[str, object]]) -> type[BaseHTTPRequestHandler]:
    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            if self.path not in ("/health", "/status"):
                self.send_response(404)
                self.end_headers()
                return
            body = json.dumps(snapshot_fn(), indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:  # noqa: A002
            return

    return HealthHandler


def create_health_server(
    gateway: LocalGateway, host: str | None = None, port: int | None = None
) -> ThreadingHTTPServer:
    bind_host = host or gateway.config.health_host
    bind_port = port if port is not None else gateway.config.health_port
    return ThreadingHTTPServer((bind_host, bind_port), make_handler(gateway.health_snapshot))
