#from turtle import screensize
from brownie import Staking, RewardToken, accounts
from scripts.deploy import deploy_all

# Test that we allow users to stake and claim rewards
def test_stake_and_claim():
    # Arrange
    ## Initial variables
    seconds_in_a_day = 86400
    seconds_in_a_year = 31449600
    deployer_address = accounts[0]
    stake_amount = 100000
    initial_supply = 1000000000000000000000000

    ## Deploy required contracts
    contracts = deploy_all(deployer_address)

    ## Map contracts to vars
    reward_token = contracts[0]
    staking_token = contracts[1]
    staking_contract = contracts[2]

    # Act 
    ## Read initial supply from token contracts
    staking_token_total_supply = staking_token.totalSupply({"from": deployer_address})
    reward_token_total_supply = reward_token.totalSupply({"from": deployer_address})

    ## Send x staking tokens to "user" wallet
    
    #send_stake_tokens = staking_token.Transfer

    ## Approve x tokens for staking on staking address
    
    ## Stake max approved tokens; print earned tokens (should be 0)
    #stake_tokens = Staking.stake(stake_amount)

    ## Move forward a certain number of blocks/ amount of time prior to claiming

    ## Claim rewards tokens 

    # Assert
    assert staking_token_total_supply == 1000000000000000000000000, "Staking token's total supply is wrong"
    assert reward_token_total_supply == 1000000000000000000000000, "Reward token's total supply is wrong"
    pass

    
    
