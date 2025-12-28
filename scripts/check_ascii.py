import sys
import tokenize


def is_ascii(s):
    try:
        s.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False


def check_ascii_file(filename):
    with open(filename, 'rb') as f:
        tokens = tokenize.tokenize(f.readline)
        for token in tokens:
            if token.type in (tokenize.COMMENT, tokenize.STRING):
                continue  # Allow Unicode in comments/strings
            if token.type == tokenize.ENCODING:
                continue
            if token.type == tokenize.ENDMARKER:
                break
            if not is_ascii(token.string):
                print(f"Non-ASCII character found in code: {filename} line {token.start[0]} col {token.start[1]}: {repr(token.string)}")
                return False
    return True


def main():
    failed = False
    for filename in sys.argv[1:]:
        if not check_ascii_file(filename):
            failed = True
    if failed:
        sys.exit(1)

if __name__ == "__main__":
    main()
