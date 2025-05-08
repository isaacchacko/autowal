import argparse
import autowal

def main():
    p = argparse.ArgumentParser(prog='autowal')
    subs = p.add_subparsers(dest='cmd')

    subs.add_parser('poll', help="Manually polls wallhaven.cc for new wallpapers")
    subs.add_parser('roll', help="Picks a new random wallpaper")
    subs.add_parser('config', help="Displays current configuration settings")
    
    args = p.parse_args()

    if args.cmd == 'poll':
        autowal.poll()

    if args.cmd == 'roll':
        autowal.pick()
    
    if args.cmd == 'config':
        autowal.show_config() 
        
    if args.cmd is None:
        autowal.main()

if __name__ == '__main__':
    main()
