from __future__ import annotations

from rock_kb.private_leakage import find_leaks


def test_find_leaks_blocks_private_fields_and_paths():
    leaks = find_leaks(
        {
            "claim": "Reviewed public claim.",
            "private_corpus_pointer": {"kind": "media_transcript"},
            "source_refs": [{"url": "https://example.org"}],
            "live_verification": {
                "evidence_refs": [
                    {"path": "data/review/live-verification-evidence/example.md"},
                ]
            },
        }
    )

    assert any("private_corpus_pointer" in leak for leak in leaks)
    assert any("data/review/" in leak for leak in leaks)


def test_find_leaks_blocks_direct_or_tokenized_media_urls():
    leaks = find_leaks({"claim": "Reviewed public claim.", "source_refs": [{"url": "https://player.vimeo.com/external/private.m3u8?oauth2_token_id=secret"}]})

    assert any("direct/tokenized media URL" in leak for leak in leaks)


def test_find_leaks_blocks_raw_transcript_markers_and_secrets():
    leaks = find_leaks({"claim": "Speaker 1: this is copied transcript text", "source_refs": [{"url": "https://example.org?access_token=secret"}]})

    assert any("raw transcript" in leak for leak in leaks)
    assert any("access_token" in leak or "direct/tokenized media URL" in leak for leak in leaks)
