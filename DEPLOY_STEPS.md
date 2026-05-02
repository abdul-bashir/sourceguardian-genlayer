# Exact Step-by-Step GenLayer Contract Creation

## A. Portal onboarding checklist

1. Connect wallet.
2. Connect GitHub.
3. Star the boilerplate repo.
4. Add GenLayer Testnet Chain.
5. Add Studio Network.
6. Claim testnet GEN.
7. Open Studio or use CLI.
8. Deploy your first contract.
9. Submit your contribution.

## B. Using GenLayer Studio

1. Open https://studio.genlayer.com
2. Connect the same wallet used in the portal.
3. Create or open a contract file.
4. Paste `contracts/source_guardian.py`.
5. Deploy with constructor args:
   - claim
   - source_a
   - source_b
   - source_c
6. Copy the contract address.
7. Run `resolve()` from Studio.
8. Run/read `get_summary()`.
9. Screenshot the deployment and result.
10. Submit on https://portal.genlayer.foundation.

## C. Using CLI

```bash
npm install -g genlayer
genlayer network testnet-bradbury
```

Deploy:

```bash
genlayer deploy \
  --contract contracts/source_guardian.py \
  --args \
  "GenLayer's Asimov and Bradbury testnets are live and focused on AI/LLM-based consensus testing." \
  "https://www.genlayer.com/testnet" \
  "https://docs.genlayer.com/developers/networks" \
  "https://venturebeat.com/business/genlayer-launches-a-new-method-to-incentivize-people-to-market-your-brand-using-ai-and-blockchain"
```

Run verification:

```bash
genlayer write <CONTRACT_ADDRESS> resolve
```

Read result:

```bash
genlayer call <CONTRACT_ADDRESS> get_summary
```

## D. GitHub repo structure

Recommended:

```text
sourceguardian-genlayer/
  contracts/
    source_guardian.py
  README.md
  SUBMISSION_TEMPLATE.md
  DEPLOY_STEPS.md
```

## E. Submission tips

Do not submit only a screenshot. Submit:
- GitHub link
- contract address
- transaction hash
- screenshots
- explanation of why it is GenLayer-specific
