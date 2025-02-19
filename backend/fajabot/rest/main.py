from datetime import datetime

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route

from fajabot.driver import get_obs_events


async def obsalerts(request):
    now = datetime.now()
    if not request.query_params.get("time"):
        return JSONResponse(
            {
                "elements": [],
                "time": now.isoformat(),
            }
        )

    fromtime = datetime.fromisoformat(request.query_params["time"])

    return JSONResponse(
        {
            "elements": get_obs_events(fromtime),
            "time": now.isoformat(),
        }
    )

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*']),
]

app = Starlette(
    debug=True,
    routes=[
        Route("/obsalerts", obsalerts),
    ],
    middleware=middleware,
)
