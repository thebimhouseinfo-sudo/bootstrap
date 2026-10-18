# Continue: optional provider/model selection

Prebuilt `agents/<role>/config.yaml` files hold the entire role instructions and a `models: []` slot. Continue does not share Codex/Claude native named-agent semantics.

Nominate the best accessible **tool-capable** model for Planner/Reviewer/Critic/Fixer; a balanced tool-capable model for Coder/Tester; a fast model for Explorer. Obtain the user's provider/model choice, fill only the relevant model block (`name`, `provider`, `model` and appropriate `roles`), and use supported secret handling. Verify loading and agent tool support. The primary chat selection remains user-controlled.
