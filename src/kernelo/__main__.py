"""Entry point: `python -m kernelo` or the `kernelo` console script."""
import asyncio

from .app import main


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run()
