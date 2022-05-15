from brownie import Staking, RewardToken, accounts

def deploy_reward_token(deployer_address):
    reward_token = RewardToken.deploy({"from": deployer_address}) 
    return reward_token

def deploy_staking_token(deployer_address):
    staking_token = RewardToken.deploy({"from": deployer_address}) 
    return staking_token

def deploy_staking_contract(deployer_address, staking_token, reward_token):
    # args passed into deploy() are required due to the constructor defined in the contract
    staking = Staking.deploy(staking_token, reward_token, {"from": deployer_address}) 
    return staking


def deploy_all(deployer_address):
    # Deploy ERC20 tokens 
    reward_token = deploy_reward_token(deployer_address)
    reward_token_address = reward_token.address
    staking_token = deploy_staking_token(deployer_address)
    staking_token_address = staking_token.address
    
    # Deploy staking contract using ERC20 addresses from above
    staking_contract = deploy_staking_contract(deployer_address, staking_token_address, reward_token_address)

    return reward_token, staking_token, staking_contract

def main():
    deployer_address = accounts[0]
    deploy_all(deployer_address)

if __name__ == "__main__":
    main()
