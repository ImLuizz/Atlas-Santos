import argparse
import asyncio
import logging
import signal
import sys

from app.core.config import settings
from app.core.logging import setup_logging
from app.worker.dispatcher import dispatcher

logger = logging.getLogger("worker")
running = True


def handle_stop_signal(sig, frame):  # noqa: ANN001
    global running
    logger.info(f"Received stop signal ({sig}). Terminating worker cleanly...")
    running = False


async def run_worker(poll_interval: float = 2.0, single_pass: bool = False) -> None:
    """Main worker execution loop."""
    logger.info(
        f"Starting Atlas Santos Worker [{settings.ENVIRONMENT}] "
        f"(poll_interval={poll_interval}s, single_pass={single_pass})"
    )

    while running:
        try:
            processed = await dispatcher.fetch_and_process_next()
            if not processed:
                if single_pass:
                    logger.info("Single-pass completed with no pending jobs. Exiting.")
                    break
                await asyncio.sleep(poll_interval)
        except asyncio.CancelledError:
            logger.info("Worker task cancelled.")
            break
        except Exception as exc:
            logger.error(f"Error in worker processing loop: {exc}")
            if single_pass:
                break
            await asyncio.sleep(poll_interval)

    logger.info("Atlas Santos Worker stopped gracefully.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Atlas Santos Background Worker")
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=2.0,
        help="Seconds to wait between database polls when idle (default: 2.0)",
    )
    parser.add_argument(
        "--single-pass",
        action="store_true",
        help="Run one polling pass and terminate (useful for testing or batch runs)",
    )
    args = parser.parse_args()

    setup_logging()

    signal.signal(signal.SIGINT, handle_stop_signal)
    signal.signal(signal.SIGTERM, handle_stop_signal)

    try:
        asyncio.run(
            run_worker(poll_interval=args.poll_interval, single_pass=args.single_pass)
        )
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
