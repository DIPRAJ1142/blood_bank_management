const patient = artifacts.require("Patient");
module.exports = function(deployer) {
   deployer.deploy(patient);
}