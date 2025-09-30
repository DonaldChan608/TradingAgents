import time
import random
import logging
from typing import Callable, Iterable, Tuple, Type, Any


class Retry:
    def __init__(
        self,
        max_attempts: int | None = 3,
        initial_backoff_seconds: float = 1.0,
        backoff_multiplier: float = 2.0,
        retry_exceptions: Tuple[Type[BaseException], ...] = (Exception,),
        jitter_seconds: float = 0.0,
        logger: logging.Logger | None = None,
    ) -> None:
        if max_attempts is not None and max_attempts < 1:
            raise ValueError("max_attempts must be >= 1 or None for unlimited")
        if initial_backoff_seconds < 0:
            raise ValueError("initial_backoff_seconds must be >= 0")
        if backoff_multiplier < 1:
            raise ValueError("backoff_multiplier must be >= 1")
        if jitter_seconds < 0:
            raise ValueError("jitter_seconds must be >= 0")

        self.max_attempts = max_attempts
        self.initial_backoff_seconds = initial_backoff_seconds
        self.backoff_multiplier = backoff_multiplier
        self.retry_exceptions = retry_exceptions
        self.jitter_seconds = jitter_seconds
        self.logger = logger

    def run(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """
        Execute func with retries using exponential backoff.

        Args:
            func: Callable to execute.
            *args: Positional args passed to func.
            **kwargs: Keyword args passed to func.

        Returns:
            The result of func(*args, **kwargs) if successful.

        Raises:
            The last exception if all attempts fail.
        """

        backoff_seconds = self.initial_backoff_seconds
        last_exc: BaseException | None = None

        attempt_number = 1
        while True:
            try:
                return func(*args, **kwargs)
            except self.retry_exceptions as exc:  # type: ignore[misc]
                last_exc = exc
                if self.max_attempts is not None and attempt_number >= self.max_attempts:
                    if self.logger:
                        self.logger.error(f"Final attempt {attempt_number} failed: {exc}")
                    raise
                if self.logger:
                    self.logger.warning(f"Attempt {attempt_number} failed: {exc}. Retrying in {backoff_seconds} seconds...")
                sleep_seconds = backoff_seconds
                if self.jitter_seconds > 0:
                    sleep_seconds += random.uniform(0, self.jitter_seconds)
                time.sleep(sleep_seconds)
                backoff_seconds *= self.backoff_multiplier
                attempt_number += 1

        # Should not reach here; loop either returned or raised
        if last_exc is not None:
            raise last_exc
        raise RuntimeError("Retry.run exited unexpectedly without result or exception")


