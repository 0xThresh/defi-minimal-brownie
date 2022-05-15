from brownie import Staking, RewardToken, accounts

# define address to deploy all contracts from 
deployer_address = accounts[0]

def deploy_reward_token(deployer_address):
    reward_token = RewardToken.deploy({"from": deployer_address}) 
    return reward_token.address

def deploy_staking_token(deployer_address):
    staking_token = RewardToken.deploy({"from": deployer_address}) 
    return staking_token.address

def deploy_staking_contract(deployer_address, staking_token, reward_token):
    # args passed into deploy() are required due to the constructor defined in the contract
    staking = Staking.deploy(staking_token, reward_token, {"from": deployer_address}) 
    return staking


def main():
    reward = deploy_reward_token(deployer_address)
    staking = deploy_staking_token(deployer_address)
    
    deploy_staking_contract(deployer_address, staking, reward)