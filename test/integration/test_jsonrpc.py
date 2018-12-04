import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from crowdclassicd import CRowdCLassicDaemon
from crowdclassic_config import CRowdCLassicConfig


def test_crowdclassicd():
    config_text = CRowdCLassicConfig.slurp_config_file(config.crowdclassic_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000007db550074c6535ce41c2a6043d0afbc86f17f1762b06e2cd65d100f7b5f'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000a8d0db898c786060f839e63529700bd00e4708b028206a8a60f391566d8'

    creds = CRowdCLassicConfig.get_rpc_creds(config_text, network)
    crowdclassicd = CRowdCLassicDaemon(**creds)
    assert crowdclassicd.rpc_command is not None

    assert hasattr(crowdclassicd, 'rpc_connection')

    # CRowdCLassic testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = crowdclassicd.rpc_command('getinfo')
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
    assert crowdclassicd.rpc_command('getblockhash', 0) == genesis_hash
