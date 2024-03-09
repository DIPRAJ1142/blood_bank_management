// const Blood = artifacts.require("faucet");
// module.exports = function(deployer) {
//    deployer.deploy(Blood);
// }

const Proof1 = artifacts.require("Blood1");
module.exports = function(deployer) {
  deployer.deploy(Proof1);
};