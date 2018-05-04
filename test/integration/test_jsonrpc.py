import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from ucomd import UCOMDaemon
from ucom_config import UCOMConfig


def test_ucomd():
    config_text = UCOMConfig.slurp_config_file(config.ucom_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000006a7203672b4f38bce10a731f8b3f45b6d32e41cc55bc35bc19a73c0a11'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'0000083f8eb64445c14163e8b28cea2214f109e3ea2bdbb7d77b2192bb75fbc7'

    creds = UCOMConfig.get_rpc_creds(config_text, network)
    ucomd = UCOMDaemon(**creds)
    assert ucomd.rpc_command is not None

    assert hasattr(ucomd, 'rpc_connection')

    # UCOM testnet block 0 hash == 0000083f8eb64445c14163e8b28cea2214f109e3ea2bdbb7d77b2192bb75fbc7
    # test commands without arguments
    info = ucomd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert ucomd.rpc_command('getblockhash', 0) == genesis_hash
