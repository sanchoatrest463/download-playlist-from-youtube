# download-playlist-from-youtube

Download YouTube playlists or single videos using [yt-dlp](https://github.com/yt-dlp/yt-dlp).

Single videos auto-detect and save flat in the output directory. Playlists get organised into subdirectories with numbered files.

## Requirements

- Python 3.8+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (`pip install yt-dlp`)
- ffmpeg (for mp3 extraction, time clipping, and metadata embedding)

## Install

```bash
pip install yt-dlp
# ffmpeg — pick your OS:
#   Debian/Ubuntu:  sudo apt install ffmpeg
#   macOS:          brew install ffmpeg
#   Windows:        choco install ffmpeg
```

## Usage

```
python main.py [options] URL
```

### Examples

```bash
# Single video → mp4 (default)
python main.py https://www.youtube.com/watch?v=XKpUzQFjtVw

# Single video → mp3
python main.py --mp3 https://www.youtube.com/watch?v=XKpUzQFjtVw

# Clip a section → mp3 (times in seconds, MM:SS, or HH:MM:SS)
python main.py --mp3 --start 1:30 --end 3:45 https://www.youtube.com/watch?v=XKpUzQFjtVw

# Full playlist → mp4
python main.py https://www.youtube.com/playlist?list=PL...

# Full playlist → mp3
python main.py --mp3 https://www.youtube.com/playlist?list=PL...

# Custom output directory
python main.py --mp3 -o ~/Music https://www.youtube.com/watch?v=XKpUzQFjtVw
```

### Options

| Flag | Description |
|---|---|
| `--mp3` | Extract audio as mp3 (192 kbps) instead of mp4 video |
| `--start TS` | Start time for clipping. Requires `--end` |
| `--end TS` | End time for clipping. Requires `--start` |
| `-o, --outdir DIR` | Output directory (default: `downloads`) |
| `--format FMT` | yt-dlp format string (default: `bv*+ba/b`) |
| `--subs langs` | Subtitle languages, comma-separated (e.g. `en,es`) |
| `--auto-subs` | Try automatic subtitles if no manual ones |
| `--rate KBPS` | Rate limit (e.g. `2M`, `500K`) |
| `--proxy URL` | Proxy (e.g. `socks5://127.0.0.1:1080`) |
| `--cookies PATH` | Path to cookies.txt for restricted videos |
| `--concurrent N` | Concurrent fragment downloads (default: 1) |
| `--retries N` | Retry attempts on network errors (default: 10) |
| `--skip-existing` | Skip files already present without using archive.txt |

### Timestamp formats for `--start` / `--end`

- Seconds: `90`
- `MM:SS`: `1:30`
- `HH:MM:SS`: `0:01:30`

### Output structure

```
downloads/
├── Video Title.mp3              ← single video
└── Playlist Name/
    ├── 001 - First Video.mp4
    ├── 002 - Second Video.mp4
    └── archive.txt              ← skip already-downloaded
```
