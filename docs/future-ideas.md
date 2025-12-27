# Future Ideas

## Agent Network Discovery Protocol

Discovered: 2025-12-27

URL: https://onetimesecret.com/.well-known/agent-network.json

A `.well-known` endpoint for agent-to-agent communication infrastructure. Enables:
- Message passing between agents
- Peer discovery across domains
- Topic-based pub/sub
- Ephemeral secret sharing
- Context handoff between agents

Auth uses CIBA (human-in-the-loop approval). Messages self-destruct.

### Potential Zociety Integration

| Current (git-based) | Could Add (network-based) |
|---------------------|---------------------------|
| Single repo scope | Cross-repo agent discovery |
| Async via commits | Real-time messaging |
| Permanent history | Ephemeral coordination |

Worth exploring if zociety agents need to coordinate beyond a single repository.

Status: experimental/draft-01
