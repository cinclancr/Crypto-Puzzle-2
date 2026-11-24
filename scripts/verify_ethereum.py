#!/usr/bin/env python3
"""Offline, dependency-free research oracle for raw Ethereum keys.

CAUTION: Accepts a private key only for locally authorized public puzzle research.
It intentionally never prints the candidate key. No broadcast or network calls.
"""
from __future__ import annotations
import argparse
import re

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (
    55066263022277343669578718895168534326250603453777594175500187360389116729240,
    32670510020758816978083085130507043184471273380659243275938904335757337482424,
)
RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
    0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
    0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
    0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
    0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
    0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
    0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
]
R = [
    [0, 36, 3, 41, 18],
    [1, 44, 10, 45, 2],
    [62, 6, 43, 15, 61],
    [28, 55, 25, 21, 56],
    [27, 20, 39, 8, 14],
]
MASK = (1 << 64) - 1


def rot(v: int, k: int) -> int:
    return ((v << k) | (v >> (64 - k))) & MASK if k else v


def keccak_f(a: list[int]) -> None:
    for rc in RC:
        c = [a[x] ^ a[x+5] ^ a[x+10] ^ a[x+15] ^ a[x+20] for x in range(5)]
        d = [c[(x-1) % 5] ^ rot(c[(x+1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                a[x+5*y] ^= d[x]
        b = [0] * 25
        for x in range(5):
            for y in range(5):
                b[y + 5 * ((2*x+3*y) % 5)] = rot(a[x+5*y], R[x][y])
        for x in range(5):
            for y in range(5):
                a[x+5*y] = b[x+5*y] ^ ((~b[(x+1) % 5+5*y]) & b[(x+2) % 5+5*y])
        a[0] ^= rc
        for i in range(25):
            a[i] &= MASK


def keccak256(msg: bytes) -> bytes:
    """Legacy Ethereum Keccak-256, domain suffix 0x01, not hashlib.sha3_256."""
    rate = 136
    data = bytearray(msg)
    data.append(0x01)
    while len(data) % rate != rate-1:
        data.append(0)
    data.append(0x80)
    lanes = [0] * 25
    for offset in range(0, len(data), rate):
        block = data[offset:offset+rate]
        for i in range(rate//8):
            lanes[i] ^= int.from_bytes(block[8*i:8*i+8], 'little')
        keccak_f(lanes)
    return b''.join(v.to_bytes(8, 'little') for v in lanes)[:32]


def add(p, q):
    if p is None:
        return q
    if q is None:
        return p
    if p[0] == q[0] and (p[1]+q[1]) % P == 0:
        return None
    if p == q:
        if p[1] == 0:
            return None
        slope = (3*p[0]*p[0] * pow(2*p[1], -1, P)) % P
    else:
        slope = ((q[1]-p[1]) * pow((q[0]-p[0]) % P, -1, P)) % P
    x = (slope*slope-p[0]-q[0]) % P
    return x, (slope*(p[0]-x)-p[1]) % P


def scalar_multiply(k: int):
    if not 1 <= k < N:
        raise ValueError('Private key must be 1 <= d < secp256k1 subgroup order')
    result = None
    base = G
    while k:
        if k & 1:
            result = add(result, base)
        base = add(base, base)
        k >>= 1
    return result


def private_key_to_address(hex_key: str) -> str:
    k = hex_key.removeprefix('0x').removeprefix('0X')
    if not re.fullmatch('[0-9a-fA-F]{64}', k):
        raise ValueError('Exactly 64 hexadecimal digits required')
    pub = scalar_multiply(int(k, 16))
    raw = pub[0].to_bytes(32, 'big') + pub[1].to_bytes(32, 'big')
    return '0x' + keccak256(raw)[-20:].hex()


PUZZLE1_KEY = '4487FC620AD0C4C67E80BE342B2EA1F5A3DC482BE6FB9C2451007322EA8BE35F'
PUZZLE1_ADDRESS = '0xc99a54eea6036115f913a13d6606e935bca47a8f'
PUZZLE2_TARGET = '0x1fa8be9de5bbfe047c72db8e8e3257128f7661ad'


def selftest() -> None:
    assert keccak256(b'').hex() == 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470', 'Keccak empty vector failed'
    assert keccak256(b'abc').hex() == '4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45', 'Keccak abc vector failed'
    assert private_key_to_address(PUZZLE1_KEY).lower() == PUZZLE1_ADDRESS, 'Historical Puzzle 1 oracle failed'
    assert private_key_to_address('0'*63+'1') == '0x7e5f4552091a69125d5dfcb7b8c2659029395bdf', 'Private-key 1 test vector failed'
    print('PASS: legacy Keccak and secp256k1 Ethereum oracle positive controls')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('--candidate', help='64-hex private-key candidate (avoid shell history in sensitive cases)')
    parser.add_argument('--target', default=PUZZLE2_TARGET)
    args = parser.parse_args()
    if args.selftest:
        selftest()
    if args.candidate:
        derived = private_key_to_address(args.candidate)
        print('Derived address:', derived)
        print('Matches configured inferred Puzzle 2 target:', derived.lower() == args.target.lower())
    if not args.selftest and not args.candidate:
        parser.print_help()


if __name__ == '__main__':
    main()
