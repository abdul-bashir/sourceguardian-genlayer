# SourceGuardian — GenLayer Evidence Verification Contract

SourceGuardian is an intelligent contract for GenLayer that verifies whether public sources support, refute, or fail to establish a claim.

## Why this is a good GenLayer builder submission

This project demonstrates GenLayer-specific capabilities rather than a generic smart contract:

- Web access with `gl.nondet.web.get()`
- LLM reasoning with `gl.nondet.exec_prompt()`
- Consensus over non-deterministic output with `gl.vm.run_nondet_unsafe()`
- Persistent state storage
- Structured, auditable result: `SUPPORTED`, `REFUTED`, or `INCONCLUSIVE`

## Contract file

`contracts/source_guardian.py`

## Suggested test deployment

Use a claim and stable URLs. Example:

Claim:

```text
GenLayer's Asimov and Bradbury testnets are live and focused on AI/LLM-based consensus testing.
```

Sources:

```text
https://www.genlayer.com/testnet
https://docs.genlayer.com/developers/networks
https://venturebeat.com/business/genlayer-launches-a-new-method-to-incentivize-people-to-market-your-brand-using-ai-and-blockchain
```

## CLI deployment

```bash
npm install -g genlayer

genlayer network testnet-bradbury

genlayer deploy \
  --contract contracts/source_guardian.py \
  --args \
  "GenLayer's Asimov and Bradbury testnets are live and focused on AI/LLM-based consensus testing." \
  "https://www.genlayer.com/testnet" \
  "https://docs.genlayer.com/developers/networks" \
  "https://venturebeat.com/business/genlayer-launches-a-new-method-to-incentivize-people-to-market-your-brand-using-ai-and-blockchain"
```

Save the returned contract address and transaction hash.

## Interact with the contract

Run the AI/web verification:

```bash
genlayer write <CONTRACT_ADDRESS> resolve
```

Read results:

```bash
genlayer call <CONTRACT_ADDRESS> get_summary
genlayer call <CONTRACT_ADDRESS> get_verdict
genlayer call <CONTRACT_ADDRESS> get_confidence
genlayer call <CONTRACT_ADDRESS> get_rationale
```

## Portal submission evidence

Submit these on the GenLayer portal:

- GitHub repo link
- Contract address
- Deployment transaction hash
- Screenshot of successful deployment
- Screenshot of `get_summary()` result
- Short explanation of what the contract does
