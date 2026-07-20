#!/usr/bin/env python3
"""Creation Date: 2024-09-28
Last Modified: 2026-07-20
Description: Download YouTube playlists or single videos as mp4 (default) or mp3.
Author: enigmak9
"""
import argparse
import os
from yt_dlp import YoutubeDL


def _is_single_video(url):
    """Return True if `url` points to a single video, not a playlist."""
    return "/watch" in url or "youtu.be/" in url or "/shorts/" in url


def _parse_timestamp(s):
    """Parse a timestamp like 1:23, 0:05:30, or 90 (seconds) into total seconds."""
    parts = s.strip().split(":")
    if len(parts) == 1:
        return int(parts[0])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    raise argparse.ArgumentTypeError(
        f"invalid timestamp '{s}'. Use seconds, MM:SS, or HH:MM:SS."
    )


def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube playlists or single videos as mp4 (default) or mp3.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""examples:
  python main.py https://www.youtube.com/watch?v=XKpUzQFjtVw
      Download a single video as mp4 (default).

  python main.py --mp3 https://www.youtube.com/watch?v=XKpUzQFjtVw
      Download a single video as mp3 audio.

  python main.py --mp3 --start 1:30 --end 3:45 https://www.youtube.com/watch?v=XKpUzQFjtVw
      Download only from 1:30 to 3:45 as mp3.

  python main.py --start 0:00 --end 5:00 https://www.youtube.com/watch?v=XKpUzQFjtVw
      Download the first 5 minutes as mp4.

  python main.py https://www.youtube.com/playlist?list=PL...
      Download an entire playlist as mp4 videos.

  python main.py --mp3 https://www.youtube.com/playlist?list=PL...
      Download an entire playlist as mp3 audio.

  python main.py --mp3 -o ~/Music https://www.youtube.com/watch?v=XKpUzQFjtVw
      Download as mp3 into ~/Music.""",
    )
    parser.add_argument("url", help="Playlist or video URL")
    parser.add_argument("-o", "--outdir", default="downloads",
                        help="Output directory (default: downloads)")
    parser.add_argument("--mp3", action="store_true",
                        help="Extract audio as mp3 instead of downloading mp4 video")
    parser.add_argument("--start", type=_parse_timestamp, default=None, metavar="TS",
                        help="Start time (seconds, MM:SS, or HH:MM:SS). Requires --end.")
    parser.add_argument("--end", type=_parse_timestamp, default=None, metavar="TS",
                        help="End time (seconds, MM:SS, or HH:MM:SS). Requires --start.")
    parser.add_argument("--format", default="bv*+ba/b",
                        help=("yt-dlp format string (default: bv*+ba/b). "
                              "Example: 'bestvideo[height<=1080]+bestaudio/best'"))
    parser.add_argument("--subs", default="", metavar="langs",
                        help=("Subtitle language codes, comma separated. "
                              "Example: en,es. Empty = no subtitles"))
    parser.add_argument("--auto-subs", action="store_true",
                        help="Try automatic subtitles if no manual ones")
    parser.add_argument("--rate", default=None, metavar="KBPS",
                        help="Rate limit, e.g. 2M, 500K")
    parser.add_argument("--proxy", default=None,
                        help="Proxy, e.g. socks5://127.0.0.1:1080")
    parser.add_argument("--cookies", default=None,
                        help="Path to cookies.txt (for age/region restricted videos)")
    parser.add_argument("--concurrent", type=int, default=1,
                        help="Concurrent fragment downloads per video (default: 1)")
    parser.add_argument("--retries", type=int, default=10,
                        help="Retry attempts on network errors (default: 10)")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip files already present without using archive.txt")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    single = _is_single_video(args.url)

    # Output template: flat for single videos, playlist-subdir for playlists
    if single:
        outtmpl = os.path.join(args.outdir, "%(title)s.%(ext)s")
    else:
        outtmpl = os.path.join(
            args.outdir, "%(playlist_title,playlist)s/%(playlist_index)03d - %(title)s.%(ext)s"
        )

    archive_path = os.path.join(args.outdir, "archive.txt")

    ydl_opts = {
        "outtmpl": outtmpl,
        "format": args.format,
        "ignoreerrors": True,
        "retries": args.retries,
        "fragment_retries": args.retries,
        "concurrent_fragment_downloads": max(1, args.concurrent),
        "noplaylist": single,
        "postprocessors": [
            {"key": "FFmpegMetadata"},
            {"key": "EmbedThumbnail"},
        ],
    }

    if args.mp3:
        ydl_opts["postprocessors"].append({
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        })
    else:
        ydl_opts["merge_output_format"] = "mp4"

    # Time range clipping
    if (args.start is None) != (args.end is None):
        parser.error("--start and --end must be used together.")
    if args.start is not None:
        # ponytail: download_ranges callback; yt-dlp passes (info_dict, ydl)
        def _range_cb(_info_dict, _ydl):
            return [{"start_time": args.start, "end_time": args.end}]
        ydl_opts["download_ranges"] = _range_cb

    # Subtitles
    if args.subs:
        langs = [s.strip() for s in args.subs.split(",") if s.strip()]
        if langs:
            ydl_opts.update({
                "writesubtitles": True,
                "subtitleslangs": langs,
                "subtitlesformat": "srt/best",
            })
    if args.auto_subs:
        ydl_opts["writeautomaticsub"] = True

    # Rate limit
    if args.rate:
        ydl_opts["ratelimit"] = args.rate

    # Proxy and cookies
    if args.proxy:
        ydl_opts["proxy"] = args.proxy
    if args.cookies:
        ydl_opts["cookiefile"] = args.cookies

    # Archive to avoid re-downloading
    if not args.skip_existing:
        ydl_opts["download_archive"] = archive_path

    # Progress hook
    def hook(d):
        if d.get("status") == "finished":
            fname = d.get("filename", "")
            print(f"✓ Finished: {os.path.basename(fname)}")

    ydl_opts["progress_hooks"] = [hook]

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([args.url])


if __name__ == "__main__":
    main()
