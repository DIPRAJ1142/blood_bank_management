const hospital = artifacts.require("Hospital");
module.exports = function(deployer) {
   deployer.deploy(hospital);
}
