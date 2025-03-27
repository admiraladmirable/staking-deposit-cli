import asyncio
import os

import click
import sys
import secrets

from staking_deposit.cli.existing_mnemonic import existing_mnemonic
from staking_deposit.cli.generate_bls_to_execution_change import generate_bls_to_execution_change
from staking_deposit.cli.new_mnemonic import new_mnemonic
from staking_deposit.utils.click import (
    captive_prompt_callback,
    choice_prompt_func,
    jit_option,
)
from staking_deposit.utils import config
from staking_deposit.utils.constants import INTL_LANG_OPTIONS
from staking_deposit.utils.intl import (
    get_first_options,
    fuzzy_reverse_dict_lookup,
    load_text,
)

# For not importing staking_deposit here
DEFAULT_VALIDATOR_KEYS_FOLDER_NAME = 'validator_keys'

def generate_password():
    with open('words.txt') as file:
        words = [word.strip() for word in file]
        return '-'.join(secrets.choice(words) for password in range(6))

async def main(argv):
    print('\n***I DO SO SOLEMNLY SWEAR THAT I WILL NEVER EVER USE THIS IN PRODUCTION***\n')
    print('\n***Using the tool on an offline and secure device is highly recommended to keep your mnemonic safe.***\n')

    nodes = int(argv[1])

    for node in range(nodes):
        my_folder_path = os.path.join(os.getcwd(), f'/tmp/node{node}')
        if not os.path.exists(my_folder_path):
            os.mkdir(my_folder_path)

        password = generate_password()
        run_script_cmd = './deposit.sh'

        cmd_args = [
            run_script_cmd,
            '--language', 'english',
            '--non_interactive',
            'new-mnemonic',
            '--num_validators', '1',
            '--mnemonic_language', 'english',
            '--chain', 'mainnet',
            '--keystore_password', password,
            '--folder', my_folder_path,
        ]

        print(cmd_args)

        proc = await asyncio.create_subprocess_shell(
            ' '.join(cmd_args),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        print('[INFO] Parsing seed phrase')
        seed_phrase = ''
        parsing = False
        async for out in proc.stdout:
            output = out.decode('utf-8').rstrip()
            if output.startswith("This is your mnemonic"):
                parsing = True
            elif output.startswith("Please type your mnemonic"):
                parsing = False
            elif parsing:
                seed_phrase += output
                if len(seed_phrase) > 0:
                    encoded_phrase = seed_phrase.encode()
                    proc.stdin.write(encoded_phrase)
                    proc.stdin.write(b'\n')
            print(output)

        async for out in proc.stderr:
            output = out.decode('utf-8').rstrip()
            print(f'[stderr] {output}')

        assert len(seed_phrase) > 0

        with open(f"{my_folder_path}/password.txt", "w") as file:
            file.write(password)

        with open(f"{my_folder_path}/mnemonic.txt", "w") as file:
            file.write(seed_phrase)


asyncio.run(main(sys.argv))
