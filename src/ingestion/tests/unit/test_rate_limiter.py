import time

from infrastructure.gateways.rate_limiter import RateLimiter


def test_first_call_does_not_wait():
    limiter = RateLimiter(max_calls_per_second=7)

    start = time.monotonic()
    limiter.wait()

    assert time.monotonic() - start < 0.05


def test_spaces_out_calls_to_respect_rate_limit():
    limiter = RateLimiter(max_calls_per_second=10)

    start = time.monotonic()
    limiter.wait()
    limiter.wait()
    elapsed = time.monotonic() - start

    assert elapsed >= 0.1


def test_does_not_wait_when_calls_are_already_spaced_out():
    limiter = RateLimiter(max_calls_per_second=10)

    limiter.wait()
    time.sleep(0.15)
    start = time.monotonic()
    limiter.wait()

    assert time.monotonic() - start < 0.05
