// const Blood1 = artifacts.require("Blood1");
// // const MetaCoin = artifacts.require("MetaCoin");
// module.exports = function(deployer) {
//   deployer.deploy(Blood1);
//   deployer.link(Blood1);
//   deployer.deploy(Blood1);
// };


const Proof = artifacts.require("Proofofexistence");
module.exports = function(deployer) {
  deployer.deploy(Proof);
};