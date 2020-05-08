from __future__ import annotations

import falcon

from application.controllers.base_controller import BaseController


class HealthCheckController(BaseController):
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.media = {"service": "healthy"}
