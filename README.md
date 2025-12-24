# 🎄 Python Christmas Tree Terminal Animation - ASCII Art

Animate a festive ASCII art Christmas tree in your terminal with blinking holiday ornaments and pulsing star!

[![Christmas in the Command Line | ASCII Tree Animation in Python](https://img.youtube.com/vi/Ji9c0Lj4kOw/maxresdefault.jpg)](https://youtu.be/Ji9c0Lj4kOw)



## 🚀 Quick Start
```bash
# Clone the repository
git clone https://github.com/artcore-c/Christmas-CLI.git ~/Christmas
cd ~/Christmas

# Run any animation
python3 Christmas_tree.py

# Press Ctrl+C to stop
```

## Features

- Pure Python (no dependencies)
- ANSI color support
- Terminal-width responsive
- Smooth animations
- Optional O Christmas Tree chiptune soundtrack (square-wave pulse channels)
- Runs in any CLI on macOS, Linux, and Windows

## 🎮 8-bit soundtrack

The animation now includes a looping chiptune rendition of **“O Christmas Tree / O Tannenbaum”** synthesized from the [BitMidi arrangement](https://bitmidi.com/o-christmas-tree-mid). All melody, harmony, and bass voices are rendered as layered square waves on the fly and played with the default system audio tools:

- macOS: `afplay`
- Linux: first available from `aplay`, `paplay`, or `ffplay`
- Windows: built-in `winsound`

### Installing a CLI player

- **macOS (Homebrew)**: `brew install ffmpeg` (installs `ffplay` if `afplay` is unavailable)
- **Ubuntu / Debian**: `sudo apt install alsa-utils` (for `aplay`) or `sudo apt install pulseaudio-utils` (for `paplay`)
- **Fedora / RHEL**: `sudo dnf install alsa-utils`
- **Arch / Manjaro**: `sudo pacman -S alsa-utils`
- **Windows**: no install required—the script uses the built-in `winsound` module.

If your machine doesn’t have one of those command-line players, the script automatically falls back to the silent animation.

Need quiet mode? Either set `CHRISTMAS_TREE_NO_AUDIO=1` or run

```bash
python3 Christmas_tree.py --no-music
```


## Want a custom terminal like ours?

Try these:
- [Hyper](https://hyper.is)
- [iTerm2](https://iterm2.com)
- [Warp](https://www.warp.dev)


## 🎁 Contributing

Feel free to submit pull requests with new holiday animations!

---

🎄 Happy Holidays! 🎄
