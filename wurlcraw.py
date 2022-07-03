import sys
import argparse
import selenium

def main():
    print("Hello!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wurlcraw, web url crawler')
    parser.add_argument('--test', action="store_true", help="Test")
    args = parser.parse_args()

    if args.test:
        print(selenium)
        sys.exit()

    main()
