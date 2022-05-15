// SPDX-License-Identifier: MIT
// stake: lock tokens into contract
// withdraw: unlock tokens from contract 
// claimReward: users get their reward tokens 
// What's a good reward mechanism? What's some good reward math? 
pragma solidity ^0.8.7;

import "./inherited/IERC20.sol";

error Staking__TransferFailed();
error Staking__NeedsMoreThanZero();

contract Staking {

    IERC20 public s_stakingToken; // s_ denotes a storage var
    IERC20 public s_rewardToken; // s_ denotes a storage var

    // address mapped to how much they staked
    mapping(address => uint256) public s_balances;

    // mapping of how much each address has been paid
    mapping(address => uint256) public s_userRewardPerTokenPaid;
    
    // mapping of how much rewards each address has to claim
    mapping(address => uint256) public s_rewards;

    uint256 public constant REWARD_RATE = 100;
    uint256 public s_totalSupply;
    uint256 public s_rewardPerTokenStored;
    uint256 public s_lastUpdateTime;

    modifier updateReward(address _account) {
        // how much reward per token?
        // last timestamp 
        // between noon and 1, user earned X tokens
        s_rewardPerTokenStored = rewardPerToken();
        s_lastUpdateTime = block.timestamp;
        s_rewards[_account] = earned(_account);
        s_userRewardPerTokenPaid[_account] = s_rewardPerTokenStored;
        _; // this tells any function to run the rest of its code here; in this case after the entire modifier has run
    }

    modifier moreThanZero(uint256 _amount) {
        if(_amount == 0) {
            revert Staking__NeedsMoreThanZero();
        }
        _;
    }

    constructor(address stakingToken, address rewardToken) {
        s_stakingToken = IERC20(stakingToken);
        s_rewardToken = IERC20(rewardToken);
    }

    function earned(address _account) public view returns(uint256) {
        uint256 currentBalance = s_balances[_account];
        // how much they have been paid already
        uint256 amountPaid = s_userRewardPerTokenPaid[_account];
        uint256 currentRewardPerToken = rewardPerToken();
        uint256 pastRewards = s_rewards[_account];

        uint256 earnedTokens = ((currentBalance * (currentRewardPerToken - amountPaid)) / 1e18) + pastRewards;
        return earnedTokens;

    }

    // based on how long it's been during this most recent snapshot
    function rewardPerToken() public view returns(uint256) {
        if(s_totalSupply == 0) {
            return s_rewardPerTokenStored;
        }
        return s_rewardPerTokenStored + (((block.timestamp - s_lastUpdateTime) * REWARD_RATE * 1e18) / s_totalSupply);
    }
    // do we allow any tokens, or just a specific token?
    //      chainlink would be needed to convert prices between tokens
    // just ETH for us
    function stake(uint256 _amount) external updateReward(msg.sender) moreThanZero(_amount) {
        // keep track of how much user has staked
        // keep track of total token supply
        // transfer tokens to this contract
        s_balances[msg.sender] = s_balances[msg.sender] + _amount;
        s_totalSupply = s_totalSupply + _amount;
        // emit event
        bool success = s_stakingToken.transferFrom(msg.sender, address(this), _amount);
        //require(success, "Staking failure");
        if(!success) {
            revert Staking__TransferFailed();
        }
    }

    function withdraw(uint256 _amount) external updateReward(msg.sender) moreThanZero(_amount) {
        s_balances[msg.sender] = s_balances[msg.sender] - _amount;
        s_totalSupply = s_totalSupply - _amount;

        bool success = s_stakingToken.transfer(msg.sender, _amount);

        if(!success) {
            revert Staking__TransferFailed();
        }
    }

    function claimReward() external updateReward(msg.sender) {
        uint256 reward = s_rewards[msg.sender];
        bool success = s_rewardToken.transfer(msg.sender, reward);
        if (!success) {
            revert Staking__TransferFailed(); 
        }
        // how much reward should they get? 

        // contract emits X tokens per second
        // disperse them to all token stakers

        // 100 tokens / second
        // 50 staked tokens / 20 / 30
        // rewards: 50, 20, 30 

        // staked: 100, 50, 20, 30
        // rewards: 50, 25, 10, 15

    }
}