from brownie import accounts, chain
from scripts.deploy import deploy_all

def test_stake_and_claim():
     
    # Arrange
    ## Initial variables
    seconds_in_a_day = 86400
    seconds_in_a_year = 31449600
    deployer_address = accounts[0]
    user_address = accounts[1]
    stake_amount = 100000000
    initial_supply = 1000000000000000000000000
    rewarded_and_withdrawn_tokens = 0
    user_address_approved = False
    user_has_reward_tokens = False

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

    ## Send all the reward tokens to the staking contract so they can be sent to users
    reward_token.transfer(staking_contract.address, initial_supply, {"from": deployer_address})

    ## Send staking tokens to "user" wallet that user can stake
    staking_token.transfer(user_address, stake_amount, {"from": deployer_address})

    ## Approve tokens for staking on staking contract
    staking_token.approve(staking_contract, stake_amount, {"from": user_address})

    ## Check that user_address has allowance set; set user_address_approved based on results
    stake_approval = staking_token.allowance(user_address, staking_contract)
    if stake_approval > 0:
        user_address_approved = True
    else:
        user_address_approved = False
    
    ## Stake max approved tokens
    staking_contract.stake(stake_amount, {"from": user_address})

    ## Move forward a certain number of blocks/ amount of time prior to claiming
    chain.sleep(seconds_in_a_day) # swap to seconds_in_a_year if desired
    chain.mine(10)

    ## Check rewards without withdrawing
    earned_tokens = staking_contract.earned(user_address)

    print("EARNED TOKENS: " + str(earned_tokens))
    if earned_tokens > 0:
        user_has_reward_tokens = True
    else: 
        user_has_reward_tokens = False

    ## Claim rewards
    staking_contract.claimReward({"from": user_address})
    rewarded_and_withdrawn_tokens = reward_token.balanceOf(user_address)

    ## Withdraw staked tokens 
    staking_contract.withdraw(stake_amount, {"from": user_address})
    withdrawn_staking_tokens = staking_token.balanceOf(user_address)

    # Assert
    assert staking_token_total_supply == 1000000000000000000000000, "Staking token's total supply is wrong"
    assert reward_token_total_supply == 1000000000000000000000000, "Reward token's total supply is wrong"
    assert user_address_approved == True, "User address is not approved for transfering staking token"
    assert user_has_reward_tokens == True, "User did not earn any tokens from staking and waiting for a certain period of time"
    assert rewarded_and_withdrawn_tokens > 0, "User did not withdraw reward tokens successfully"
    assert withdrawn_staking_tokens > 0, "User did not withdraw reward tokens successfully"



    
