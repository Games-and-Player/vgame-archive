import sys
import functools
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from web.build import build_site

DEFAULT_OUTPUT = Path(__file__).parent.parent / "dist"


def serve(host: str = "0.0.0.0", port: int = 8080, output_dir: Path = DEFAULT_OUTPUT, do_build: bool = False):
    if do_build or not output_dir.exists():
        build_site(output_dir=output_dir)

    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(output_dir))
    server = HTTPServer((host, port), handler)
    print(f"Serving {output_dir} at http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    do_build = "--build" in sys.argv
    port = 8080
    for arg in sys.argv[1:]:
        if arg.startswith("--port="):
            port = int(arg.split("=")[1])
    serve(do_build=do_build, port=port)
