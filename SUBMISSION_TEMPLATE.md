# GenLayer Portal Submission Template

## Contribution Type
Builder

## Title
SourceGuardian — Evidence-backed AI claim verifier for GenLayer

## Short Description
I built and deployed an intelligent contract that verifies whether public web sources support, refute, or fail to establish a claim. The contract uses GenLayer's web access, LLM reasoning, and custom equivalence validation to store a structured verdict on-chain.

## Detailed Description
SourceGuardian demonstrates a GenLayer-native use case: trustless, source-backed claim verification. A user deploys the contract with a claim and up to three source URLs. When `resolve()` is called, the contract fetches the sources, asks an LLM to evaluate the claim strictly using the provided evidence, validates the result across validators using a custom equivalence rule, and stores a final verdict (`SUPPORTED`, `REFUTED`, or `INCONCLUSIVE`) with confidence and rationale.

## Why it matters
This is useful for:
- DAO proposal fact checks
- RWA disclosure checks
- on-chain research attestations
- prediction-market evidence snapshots
- grants / bounty verification
- compliance or public-source due diligence

## Evidence to attach
- GitHub repo:
- Contract address:
- Deployment transaction hash:
- Screenshot 1: contract deployed
- Screenshot 2: `resolve()` transaction
- Screenshot 3: `get_summary()` result

## Technical Features Used
- `gl.Contract`
- `@gl.public.write`
- `@gl.public.view`
- `gl.nondet.web.get()`
- `gl.nondet.exec_prompt()`
- `gl.vm.run_nondet_unsafe()`
- custom validator function for non-deterministic consensus
- persistent state variables

## Suggested deployed test case
Claim:
GenLayer's Asimov and Bradbury testnets are live and focused on AI/LLM-based consensus testing.

Sources:
1. https://www.genlayer.com/testnet
2. https://docs.genlayer.com/developers/networks
3. https://venturebeat.com/business/genlayer-launches-a-new-method-to-incentivize-people-to-market-your-brand-using-ai-and-blockchain
