import importlib.util
from pathlib import Path

SCRIPT=Path(__file__).resolve().parents[1]/'scripts'/'verify_ethereum.py'
spec=importlib.util.spec_from_file_location('eth_oracle',str(SCRIPT))
oracle=importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)


def test_keccak_empty_and_abc():
    assert oracle.keccak256(b'').hex() == 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'
    assert oracle.keccak256(b'abc').hex() == '4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45'


def test_known_disclosed_puzzle1_key():
    assert oracle.private_key_to_address(oracle.PUZZLE1_KEY).lower() == oracle.PUZZLE1_ADDRESS


def test_key_one_known_vector():
    assert oracle.private_key_to_address('0'*63+'1') == '0x7e5f4552091a69125d5dfcb7b8c2659029395bdf'
