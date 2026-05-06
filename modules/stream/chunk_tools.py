"""
Name: Stream Chunk Tools (no deps)

Why:
- Edge ASR streams usually send fixed-size audio chunks
- Chunk metadata helps debug latency and dropped packets

Features:
- chunk size calculation
- byte chunk iteration
- sequence numbers
- jitter and latency helpers
- real-time factor calculation

Limitations:
- Does not open sockets
- Works with already-captured bytes
"""


def bytes_per_chunk(sample_rate=16000, sample_width=2, channels=1, chunk_ms=100):
    return int(sample_rate * sample_width * channels * chunk_ms / 1000)


def iter_byte_chunks(data, chunk_size):
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def chunk_count(byte_count, chunk_size):
    return (byte_count + chunk_size - 1) // chunk_size


def sequence_chunks(chunks, start=0):
    return [{"seq": start + i, "data": chunk} for i, chunk in enumerate(chunks)]


def missing_sequences(received):
    received = sorted(received)
    if not received:
        return []
    expected = set(range(received[0], received[-1] + 1))
    return sorted(expected - set(received))


def chunk_timestamp(seq, chunk_ms):
    return seq * chunk_ms / 1000.0


def latency_ms(sent_time, received_time):
    return (received_time - sent_time) * 1000.0


def jitter_ms(latencies):
    latencies = list(latencies)
    if len(latencies) < 2:
        return 0
    diffs = [abs(b - a) for a, b in zip(latencies, latencies[1:])]
    return sum(diffs) / len(diffs)


def real_time_factor(process_seconds, audio_seconds):
    return process_seconds / float(audio_seconds) if audio_seconds else 0


def should_backpressure(queue_size, max_queue):
    return queue_size >= max_queue


def drop_oldest(queue, keep):
    return list(queue)[-keep:] if keep > 0 else []


if __name__ == "__main__":
    print("[TEST] chunk_tools")
    try:
        assert bytes_per_chunk(chunk_ms=100) == 3200
        assert list(iter_byte_chunks(b"abc", 2)) == [b"ab", b"c"]
        assert chunk_count(5, 2) == 3
        assert sequence_chunks([b"a"], 3)[0]["seq"] == 3
        assert missing_sequences([1, 3]) == [2]
        assert chunk_timestamp(2, 100) == 0.2
        assert latency_ms(1, 1.5) == 500
        assert jitter_ms([1, 3, 6]) == 2.5
        assert real_time_factor(0.5, 1) == 0.5
        assert should_backpressure(5, 5)
        assert drop_oldest([1, 2, 3], 2) == [2, 3]
        print("[OK] chunk helpers")
        print("[DONE]")
    except Exception as e:
        print("[FAIL]", e)
