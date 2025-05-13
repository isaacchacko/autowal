# autowal

A command line interface to dynamically poll and set aesthetic wallpapers sourced from [wallhaven.cc](https://www.wallhaven.cc) while updating system-wide colors using [pywal](https://github.com/dylanaraps/pywal).

[demo.webm](https://github.com/user-attachments/assets/287378b5-2ccb-40f5-b369-5839bf341129)


## Usage

  ```bash
  autowal poll 
  ```
  - Downloads the first page of wallpapers matching the parameters found in the `config.ini` file. The first wallpaper downloaded becomes the new wallpaper. Ignores if a poll has been done in the past day.

  ```bash
  autowal roll 
  ```
  - Randomly chooses a new downloaded wallpaper to use.

  ```bash
  autowal config
  ```
  - Displays the current configuration file.

  ```bash
  autowal
  ```
  - A combination of both `poll` and `roll`. `poll` will execute if it's been at least one day since the last call. Otherwise, `roll` will choose a new wallpaper.

## Configuration

To customize the query of wallpapers from wallhaven.cc, please refer to the [documentation](https://wallhaven.cc/help/api) and update the values within `config.ini` accordingly. 

For ease of access, `autowal` can be bound to execute on startup, or by a keybind. For example, the following is the configuration for `autowal` execution when using `i3wm`, used within i3's `config` file.

  ```bash
  exec_always --no-startup-id autowal
  bindsym $mod+c exec --no-startup-id autowal
  ```

## Dependencies
  - [pywal](https://github.com/dylanaraps/pywal). Correct configuration of `pywal`'s features is critical for proper `autowal` usage

## Installation

First, try to use the pre-compiled binary:
   ```bash
   git clone https://github.com/isaacchacko/autowal.git
   sudo cp autowal/autowal /usr/local/bin/
   cp autowal/deadlock.jpg ~/Pictures/deadlock.jpg
   rm -rf autowal
   ```
If that doesn't work, try compiling locally.

1. Create and populate a virtual environment:

   ```bash
   git clone https://github.com/isaacchacko/autowal.git
   cd autowal
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Compile:

   ```bash
   pyinstaller --onefile cli.py
   sudo cp dist/cli /usr/local/bin/autowal
   cp deadlock.jpg ~/Pictures/deadlock.jpg
   cd ..
   rm -rf autowal
   ```

## Issues

There is a known issue between the [pywal](https://github.com/dylanaraps/pywal) library and Windows, especially with changing the background. Although `autowal` will still continue to download/cycle new color schemes with Windows computers, the background will not change. There is a fork of `pywal` called [winwal](https://github.com/scaryrawr/winwal) which does seem to fix matters, although this code is not incorporated into `autowal`.
