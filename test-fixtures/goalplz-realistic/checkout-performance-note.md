# Checkout Performance Note

Observed path: `src/checkout/createOrder.ts`

Current local benchmark:

```text
npm run bench -- checkout
p95 createOrder: 410ms
p50 createOrder: 145ms
sample size: 500
```

Target:

```text
p95 createOrder <= 250ms
```

Correctness checks:

```text
npm test -- src/checkout
npm run typecheck
```

Do not change payment authorization behavior or order total calculation.
