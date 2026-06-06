# TinyCache: Adaptive KV Compression for Long-Context Agents

This mock paper is a local Goalplz test fixture, not a real paper.

## Claim

TinyCache reduces agent inference memory usage while preserving answer quality on long-context retrieval tasks.

## Method

- Compress keys and values after every 4 decoding steps.
- Keep the top 20 percent attention mass uncompressed.
- Use the LongBench-QA subset as the primary benchmark.

## Table 2

| Method | LongBench-QA F1 | Peak VRAM GB | Tokens/s |
|---|---:|---:|---:|
| Baseline Transformer | 72.4 | 23.8 | 41.0 |
| Sliding Window | 69.1 | 15.2 | 58.3 |
| TinyCache | 71.8 | 14.6 | 55.7 |

## Reproduction Notes

- Dataset: local mock subset at `data/longbench_qa_tiny.jsonl`
- Metric: token-normalized F1
- Script in paper appendix: `python experiments/tinycache_eval.py --subset longbench_qa_tiny`
- Expected output artifact: `reports/tinycache_table2_repro.md`
