# AxiomHash

Small utility for streaming SHA-256 and Merkle-root helper used in the AxiomHive starter.

Usage:

- Compute sha256 of a file:

  python src/axiomhash_cli.py somefile.bin

- Compute sha256 from stdin:

  cat file | python src/axiomhash_cli.py
