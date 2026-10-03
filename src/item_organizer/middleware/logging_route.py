import time
from typing import Callable
from fastapi import Request, Response  #  FastAPI, APIRouter,
from fastapi.routing import APIRoute


# 1. Define the Custom APIRoute Class
class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            # Safely read the request body into memory
            req_body = await request.body()

            # Log the incoming request details
            print(f"--> [REQ] {request.method} {request.url.path}")
            if req_body:
                print(f"    Body: {req_body.decode('utf-8', errors='ignore')}")

            start_time = time.time()

            # Execute the actual endpoint logic
            response: Response = await original_route_handler(request)

            process_time = (time.time() - start_time) * 1000

            # Log the outgoing response details
            print(f"<-- [RES] {response.status_code} ({process_time:.2f}ms)")
            if hasattr(response, "body") and isinstance(response.body, bytes):
                try:
                    # Explicitly letting your IDE know this is a bytes object
                    body_bytes: bytes = response.body
                    print(f"    Body: {body_bytes.decode('utf-8', errors='ignore')}")
                except Exception as e:
                    print(f"    Body: [Could not decode body: {e}]")
            else:
                print("    Body: [Streaming or empty response payload]")

            return response

        return custom_route_handler
