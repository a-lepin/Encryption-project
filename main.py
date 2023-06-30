import argparse
import encryption
import cracker


def create_parser():
    """Parses command line arguments, using the argparse module, and return result."""

    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=argparse.FileType('r'))
    parser.add_argument('output', type=argparse.FileType('w'))
    parser.add_argument('language', choices=['rus', 'eng'])
    parser.add_argument('mode', choices=['encrypt', 'decrypt'])
    cipher_parsers = parser.add_subparsers(dest='cipher_name')

    caesar_parsers = cipher_parsers.add_parser('caesar')
    vigenere_parsers = cipher_parsers.add_parser('vigenere')
    verman_parsers = cipher_parsers.add_parser('verman')
    caesar_crack_parser = cipher_parsers.add_parser('crack')

    caesar_parsers.add_argument('key', type=int, nargs='?', default=3)
    vigenere_parsers.add_argument('key', type=argparse.FileType('r'))
    verman_parsers.add_argument('key', type=argparse.FileType('r+'))
    
    return parser

def process_request(args: argparse.Namespace) -> None:
    """Determines the type of request and executes the desired request."""

    encr = encryption.Encryption(args.language)

    if args.mode not in ('encrypt', 'decrypt'):
        raise ValueError('Unknown mode: {}'.format(args.mode))

    if args.cipher_name == 'caesar':
        if args.mode == 'encrypt':
           args.output.write(encr.encrypt_caesar(args.input.read(), args.key))
        else:
            args.output.write(encr.decrypt_caesar(args.input.read(), args.key))

    elif args.cipher_name == 'vigenere':
        if args.mode == 'encrypt':
            args.output.write(encr.encrypt_vigenere(args.input.read(), args.key.read()))
        else:
            args.output.write(encr.decrypt_vigenere(args.input.read(), args.key.read()))
        
    elif args.cipher_name == 'verman':
        if args.mode == 'encrypt':
            ciphertext, key = encr.encrypt_verman(args.input.read())
            args.output.write(ciphertext)
            args.key.write(key)
        else:
            args.output.write(encr.decrypt_verman(args.input.read(), args.key.read()))
    elif args.cipher_name == 'crack':
        if args.mode == 'decrypt':
            _cracker = cracker.СaesarСipherСracker(args.language)
            args.output.write(_cracker.crack_caesar(args.input.read()))
        else:
            raise ValueError('for crack you must use mode decrypt, after {}'.format(args.mode))

    else:
        raise ValueError('Unknown cipher_name: {}'.format(args.cipher_name))
        
if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    process_request(args)
