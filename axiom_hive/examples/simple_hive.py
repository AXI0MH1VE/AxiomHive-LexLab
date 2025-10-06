"""
End-to-end with hybrid proofs.
"""

import io
import torch
from axiom_hive.dag import AxiomDAG
from axiom_hive.shard import AIShard
from axiom_hive.compression import compress_model, decompress_model
from axiom_hive.sanctity import SanctityProtocol

def main():
    print("--- Initializing AxiomHive: Sovereign AI Ascent ---")

    print("Creating AIShards...")
    shard_in = AIShard(input_dim=10, output_dim=5)
    shard_mid = AIShard(input_dim=5, output_dim=3)
    shard_out = AIShard(input_dim=3, output_dim=1)

    print("Constructing Axiomatic DAG...")
    dag = AxiomDAG()
    dag.add_shard("input_shard", func=lambda: shard_in(torch.randn(1, 10)))
    dag.add_shard("middle_shard", dependencies=["input_shard"], func=lambda input_shard: shard_mid(input_shard))
    dag.add_shard("output_shard", dependencies=["middle_shard"], func=lambda middle_shard: shard_out(middle_shard))

    print("Sanctifying with 2025 LHC + Hybrid...")
    protocol = SanctityProtocol()
    try:
        blueprint = protocol.sanctify(dag)
        final_result = blueprint['blueprint']["output_shard"]
        proofs = blueprint['proofs']
        print(f"Sanctified Execution Complete. Result: {final_result}")
        print(f"Hybrid Proofs Verified: {list(proofs.keys())}")
    except ValueError as e:
        print(f"NULL_PATH: {e}")
        return

    print("\n--- Lossless Model Compression ---")
    
    original_state_dict = shard_out.state_dict()
    
    print("Compressing...")
    compressed_weights = compress_model(original_state_dict)
    buffer = io.BytesIO()
    torch.save(original_state_dict, buffer)
    original_size = buffer.tell()
    print(f"Original: {original_size} bytes | Compressed: {len(compressed_weights)} bytes")
    
    print("Decompressing...")
    decompressed_state_dict = decompress_model(compressed_weights)
    
    match_check = all(
        torch.equal(original_state_dict[key], decompressed_state_dict[key])
        for key in original_state_dict
    )
    print(f"Lossless: {match_check}")
    
    restored_shard = AIShard(input_dim=3, output_dim=1)
    restored_shard.load_state_dict(decompressed_state_dict)
    
    print("\n--- AxiomHive Example Complete ---")

if __name__ == "__main__":
    main()