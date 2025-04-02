import argparse

def main():
    parser = argparse.ArgumentParser(description='Find classes in a file containing Python subclass entries')
    parser.add_argument('file', help='Path to the file containing class entries')
    parser.add_argument('search', nargs='?', help='Search term (case-insensitive partial match)')
    parser.add_argument('-p', '--print-all', action='store_true', help='Print all classes with indices')
    args = parser.parse_args()

    try:
        with open(args.file, 'r') as f:
            data_line = f.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found")
        return
    
    elements = data_line[1:-1].split(', ')
    classes = []
    for elem in elements:
        elem = elem.strip()
        if elem.startswith("<") and elem.endswith(">"):
            # a class broke without this fix
            content = elem[1:-1].split(' ', 1)[-1].strip("'\"")
            classes.append(content)
        else:
            # some entries get messed up. here is a blanket fix.
            classes.append(elem.strip("'\""))

    if args.print_all:
        print("Full class list:")
        for idx, cls in enumerate(classes):
            print(f"{idx:4}: {cls}")

    if args.search:
        search_lower = args.search.lower()
        matches = [(i, cls) for i, cls in enumerate(classes) if search_lower in cls.lower()]
        
        if matches:
            print(f"\nFound {len(matches)} matches for '{args.search}':")
            for i, cls in matches:
                print(f"{i:4}: {cls}")
        else:
            print(f"\nNo matches found for '{args.search}'")

if __name__ == "__main__":
    main()