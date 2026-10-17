# Snapshot and restore implementation guide

Before modifying guarded code/config, capture only relevant project files with safe paths and reproducible restore instructions. Confirm git working-tree cleanliness/untracked content without discarding any work. Prove restore on disposable sample. No destructive reset, external copy, secret exposure or assumed OS command. Build actual script appropriate to verified host, shell and repository.
