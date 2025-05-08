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
