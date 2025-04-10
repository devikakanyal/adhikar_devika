const { ethers } = require("hardhat");

async function main() {
  const FIRSystem = await ethers.getContractFactory("FIRSystem");
  const contract = await FIRSystem.deploy(); // deploy the contract
  await contract.waitForDeployment(); // Wait for deployment to finish

  console.log("Contract deployed to:", await contract.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
