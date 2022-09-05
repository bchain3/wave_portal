from brownie import WavePortal, accounts, network, config


def getAccount():
    if network.show_active() == 'development':
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"]) # creates account with private key on the fly not encrypted

def functionality_test():
    # can also be done in other ways using locally created accounts using new see https://www.youtube.com/watch?v=OeHYm7CXNsw
    # account = accounts.load("metaMaskBrave")  new created account
    account = getAccount()
    wp = WavePortal.deploy({'from':account})

    # funding WavePortal contract
    account.transfer(wp.address, '0.0000001 ether')
    print('Intial contract balance is ' + str(wp.balance()))

    initial_wave_count = wp.waveCount(account)
    print('Initial wave count is ' + str(initial_wave_count))

    tx = wp.wave(account, "Sup Boys!", {'from':account})
    tx.wait(1)
    print(str(tx.events['WaveLog']['_from']) + ' waved at '  + str(tx.events['WaveLog']['_to']))

    updated_wave_count = wp.waveCount(account)
    print('Updated wave count is ' + str(updated_wave_count))


def main():
    functionality_test()
