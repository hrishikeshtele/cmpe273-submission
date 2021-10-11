def base62_encode(num):
    s = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    hash_str = ''
    while num > 0:
        hash_str = s[num % 62] + hash_str
        num //= 62
    return hash_str
