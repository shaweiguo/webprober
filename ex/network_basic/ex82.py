from loguru import logger
import hashlib


def alpha_shard(word):
    if word[0] < 'g':
        return 'server0'
    elif word[0] < 'n':
        return 'server1'
    elif word[0] < 't':
        return 'server2'
    else:
        return 'server3'

def hash_shard(word):
    return f'server{hash(word) % 4}'

def md5_shard(word):
    data = word.encode('utf-8')
    return f'server{hashlib.md5(data).digest()[-1] % 4}'

def hashing():
    words = open('./ex81.py').read().split()
    for func in alpha_shard, hash_shard, md5_shard:
        servers = {
            'server0': 0,
            'server1': 0,
            'server2': 0,
            'server3': 0
        }
        for word in words:
            servers[func(word.lower())] += 1
        logger.info(f'{func.__name__[:-6]}')
        for key, value in sorted(servers.items()):
                logger.info(f' {key} {value} {value/len(words):.2}')

def main():
    hashing()


if __name__ == '__main__':
    main()
