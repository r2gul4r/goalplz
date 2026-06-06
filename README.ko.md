<p align="right">
  <a href="./README.md">English</a> | 한국어
</p>

# Goalplz

Goalplz는 거친 요청을 안전하고 검증 가능한 Codex Goal mode 프롬프트로 컴파일해주는 Codex 플러그인이다.

재사용 가능한 `$goalplz` 스킬과 선택 설치 가능한 `/goalplz` custom prompt alias를 함께 제공한다.

## 왜 필요한가

Codex Goal mode는 목표에 구체적인 결과, 검증면, 제약, 경계, 반복 정책, blocked 정지 조건이 있을 때 가장 잘 작동한다. Goalplz는 애매한 다단계 요청을 템플릿에 끼워 넣지 않고, route와 계약을 먼저 만든 뒤 Codex가 실행하기 좋은 `/goal`, `/plan`, 질문, 일반 프롬프트, 또는 거절로 렌더링한다.

## 사용자 명령

선택 prompt alias를 설치한 뒤 권장 사용법:

```text
/goalplz 실패하는 checkout 테스트를 고치고 검증될 때까지 계속 진행해
```

Codex 표면에 따라 custom prompt가 이렇게 보일 수도 있다:

```text
/prompts:goalplz 실패하는 checkout 테스트를 고치고 검증될 때까지 계속 진행해
```

스킬을 직접 호출해도 된다:

```text
Use $goalplz to turn this request into a clear Codex goal and run it when appropriate: 실패하는 checkout 테스트를 고쳐줘
```

## 기능

- Goal mode가 맞는 도구인지 판단하고 `READY_GOAL`, `PLAN_FIRST`, `NEEDS_TIGHTENING`, `NOT_GOAL`, `REFUSE` 중 하나로 route를 고른다.
- 거친 요청에서 outcome, context, provenance, scope, verification, risk, constraints, rollback, pause trigger, completion condition을 추출한다.
- 안전하고 되돌릴 수 있는 빈칸만 추론하고, 성공 기준/권한/외부 시스템/보안/비용/프로덕션 영향은 invent하지 않는다.
- `READY_GOAL`은 사람이 읽기 쉬운 compact Markdown `/goal` 계약으로 렌더링한다.
- 준비되지 않은 요청은 `/plan`, 최대 3개의 blocking question, 일반 프롬프트, 또는 거절로 안전하게 라우팅한다.
- 현재 Codex 표면에서 goal-management 도구를 지원하면 goal을 시작하고, 직접 goal 생성이 불가능하면 바로 붙여 넣을 수 있는 명령으로 fallback한다.

## 개떡 프롬프트 변환 테스트

2026-06-06에 `test-fixtures/goalplz-realistic/` 아래에 가짜 실패 로그, 성능 메모, 논문, 코드 파일, UI 기준 이미지를 만들고 현재 `prompts/goalplz.md`와 `$goalplz` skill 규칙으로 dry-run 변환 테스트를 돌렸다.

이 테스트의 목적은 작업을 실제로 실행하는 것이 아니라, 사용자가 개떡같이 말했을 때 Goalplz가 어떤 `/goal` 프롬프트로 렌더링하는지 확인하는 것이다.

Goalplz는 내부적으로 context, provenance, scope, verification, risk, pause trigger 같은 계약 필드를 만든다. 하지만 최종 출력이 항상 `Context:`, `Scope:`, `Verification:` 같은 고정 템플릿이어야 하는 것은 아니다. 짧게 충분하면 compact `/goal` 한 덩어리로 렌더링하고, 길어지면 별도 contract 파일을 참조하는 식으로 바꿀 수 있다.

사용한 fixture:

- `test-fixtures/goalplz-realistic/checkout-failure.log`
- `test-fixtures/goalplz-realistic/checkout-performance-note.md`
- `test-fixtures/goalplz-realistic/mock-paper.md`
- `test-fixtures/goalplz-realistic/src/checkout/OrderSummary.tsx`
- `test-fixtures/goalplz-realistic/src/components/ProductCard.tsx`
- `test-fixtures/goalplz-realistic/assets/product-card-mobile-reference.svg`

### 테스트 1: 실패 로그 첨부

입력:

```text
/goalplz 첨부한 실패 로그 기준으로 테스트 깨지는듯 고쳐봐

첨부:
test-fixtures/goalplz-realistic/checkout-failure.log
```

변환된 `/goal` 프롬프트:

```text
/goal test-fixtures/goalplz-realistic/checkout-failure.log를 기준으로 실패한 checkout 테스트를 재현하고, 원인을 찾아 가장 작은 안전한 변경으로 통과시켜라. 테스트 삭제, skip, 기대값 약화는 금지한다. 수정 전 `npm test -- src/checkout/__tests__/applyCoupon.test.ts`로 baseline을 기록하고, 수정 후 같은 테스트와 관련 checkout 검증을 다시 실행한다. 실패가 재현되지 않거나 테스트를 약화해야만 풀리는 경우에는 멈추고 보고한다.
```

### 테스트 2: 성능 메모 첨부

입력:

```text
/goalplz 첨부한 성능 메모 기준으로 checkout 좀 빠르게 해줘

첨부:
test-fixtures/goalplz-realistic/checkout-performance-note.md
```

변환된 `/goal` 프롬프트:

```text
/goal test-fixtures/goalplz-realistic/checkout-performance-note.md를 source of truth로 삼아 checkout createOrder p95를 410ms에서 250ms 이하로 낮춰라. 결제 승인 동작과 주문 총액 계산은 보존하고 benchmark threshold를 임의로 바꾸지 않는다. `npm run bench -- checkout`으로 baseline과 결과를 비교하고, `npm test -- src/checkout` 및 `npm run typecheck`로 correctness를 확인한다. 목표 달성에 결제/총액 계산 변경이 필요하면 멈추고 보고한다.
```

### 테스트 3: 논문 첨부

입력:

```text
/goalplz 첨부한 논문 재현 좀 해봐. 일단 Table 2 결과 중심으로.

첨부:
test-fixtures/goalplz-realistic/mock-paper.md
```

변환된 `/goal` 프롬프트:

```text
/goal test-fixtures/goalplz-realistic/mock-paper.md를 source of truth로 삼아 TinyCache 논문의 Table 2 결과를 재현 또는 감사하고 `reports/tinycache_table2_repro.md`에 기록하라. Table 2의 F1, VRAM, Tokens/s와 reproduction notes의 dataset, metric, command를 기준으로 사용한다. 가능하면 `python experiments/tinycache_eval.py --subset longbench_qa_tiny`를 실행하고, 논문 수치와 결과 차이표, 실행 로그, 누락 조건을 남긴다. dataset, script, checkpoint, compute 조건 때문에 exact reproduction이 불가능하면 proxy evidence로 명시한다.
```

### 테스트 4: 코드 파일 지정

입력:

```text
/goalplz src/checkout/OrderSummary.tsx 좀 정리해줘. 너무 지저분함. 동작은 바꾸지 마.

대상 파일:
test-fixtures/goalplz-realistic/src/checkout/OrderSummary.tsx
```

변환된 `/goal` 프롬프트:

```text
/goal test-fixtures/goalplz-realistic/src/checkout/OrderSummary.tsx를 동작 변경 없이 읽기 쉽게 정리하라. `OrderSummaryProps`, 렌더링 의미, 금액 계산 정책을 보존하고 새 기능, 디자인 변경, public API 변경, checkout 구조 재작성은 하지 않는다. 지정 파일과 직접 필요한 helper만 수정하며, 관련 test/lint/typecheck가 있으면 실행하고 diff가 readability 개선에 한정되는지 보고한다. 동작 보존을 위해 더 큰 구조 변경이 필요하면 멈추고 보고한다.
```

### 테스트 5: UI 파일과 기준 이미지 첨부

입력:

```text
/goalplz 첨부 스샷 기준으로 ProductCard.tsx 모바일 좀 예쁘게 고쳐줘.

첨부/대상:
test-fixtures/goalplz-realistic/assets/product-card-mobile-reference.svg
test-fixtures/goalplz-realistic/src/components/ProductCard.tsx
```

변환된 `/goal` 프롬프트:

```text
/goal test-fixtures/goalplz-realistic/assets/product-card-mobile-reference.svg와 test-fixtures/goalplz-realistic/src/components/ProductCard.tsx를 기준으로 모바일 ProductCard 레이아웃을 다듬어라. desktop 동작과 기존 데이터 흐름은 보존하고, 상품 데이터 모델, cart behavior, 전체 design system은 바꾸지 않는다. 390x844 mobile viewport와 desktop viewport에서 스크린샷을 확인하고, Add to cart interaction, text overlap 없음, image alt/accessibility regression 없음을 기록한다. 기준 이미지와 기존 component contract가 충돌하면 멈추고 보고한다.
```

## 저장소 구조

```text
.agents/
  plugins/
    marketplace.json
plugins/
  goalplz/
    .codex-plugin/plugin.json
    skills/
      goalplz/
        SKILL.md
        agents/openai.yaml
        references/goal-patterns.md
prompts/
  goalplz.md
```

플러그인 루트는 `plugins/goalplz`다. 저장소 루트는 Codex용 local marketplace root로 동작한다.

## 로컬에 플러그인 설치

빠른 설치:

```bash
python scripts/install.py
python scripts/verify.py --installed
```

Codex CLI를 쓸 수 없는 환경에서도 installer는 compatibility skill과 prompt alias 설치를 계속한다. Codex plugin 등록/설치 실패 시 설치를 중단하고 싶으면 `--require-marketplace --require-plugin`을 쓴다.

기본 설치는 Goalplz skill 중복 노출을 피한다. Codex plugin이 installed/enabled로 확인되면 user-level compatibility skill fallback을 제거하고, plugin이 확인되지 않을 때만 fallback을 설치한다. plugin skill을 직접 읽지 못하는 Codex 표면에서만 `--with-compat-skill`을 쓴다.

`goalplz-local` marketplace가 다른 저장소 경로로 이미 등록되어 있으면 이렇게 갱신한다:

```bash
python scripts/install.py --replace-marketplace
```

plugin cache가 오래됐거나 잠겨 있으면 remove/add 사이클을 강제로 돌린다:

```bash
python scripts/install.py --reinstall-plugin
```

Windows에서는 installer가 WindowsApps `codex` alias보다 Codex config의 `CODEX_CLI_PATH`를 먼저 사용해서 app alias 권한 문제를 피한다.

저장소 루트에서 실행:

```bash
codex plugin marketplace add .
codex plugin add goalplz@goalplz-local
```

그 다음 Codex를 재시작한다. `goalplz`가 `Goalplz Local` marketplace의 installed plugin으로 보여야 한다.

수동 local marketplace 방식에서는 Codex가 이 파일을 읽는다:

```text
.agents/plugins/marketplace.json
```

그 marketplace는 이 플러그인을 가리킨다:

```text
./plugins/goalplz
```

설치 스크립트는 Codex plugin이 설치된 것으로 확인되지 않거나 `--with-compat-skill`을 넘긴 경우에만 `${CODEX_HOME:-~/.codex}/skills/goalplz`에 compatibility skill을 미러링한다. plugin skill과 compatibility skill을 둘 다 설치하면 skill picker에 Goalplz가 두 번 보일 수 있다.

## `/goalplz` alias 설치

Codex plugin manifest는 skill을 패키징하지만 custom prompt alias는 별도로 설치해야 한다.

PowerShell:

```powershell
$promptDir = Join-Path $env:USERPROFILE ".codex\prompts"
New-Item -ItemType Directory -Force -Path $promptDir | Out-Null
Copy-Item -Force ".\prompts\goalplz.md" (Join-Path $promptDir "goalplz.md")
```

Bash:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/prompts"
cp ./prompts/goalplz.md "${CODEX_HOME:-$HOME/.codex}/prompts/goalplz.md"
```

새 스킬이나 prompt가 바로 보이지 않으면 Codex를 재시작하거나 새 스레드를 시작한다.

전체 설치 흐름은 [INSTALL.md](./INSTALL.md)를 보면 된다.

## 유지보수

- [INSTALL.md](./INSTALL.md): Goalplz 로컬 설치와 검증.
- [UPDATE.md](./UPDATE.md): 기존 설치 업데이트.
- [UNINSTALL.md](./UNINSTALL.md): prompt alias, compatibility skill, marketplace entry 제거.
- [CONTRIBUTING.md](./CONTRIBUTING.md): 기여 범위와 검증 명령.
- [SECURITY.md](./SECURITY.md): 취약점 제보와 보안 기대사항.

## 검증

Codex skill-creator와 plugin-creator 유틸리티가 있다면 실행:

```bash
python path/to/skill-creator/scripts/quick_validate.py ./plugins/goalplz/skills/goalplz
python path/to/plugin-creator/scripts/validate_plugin.py ./plugins/goalplz
```

## 근거

이 워크플로는 공개 Codex Goal mode 가이드를 따른다. 목표는 지속적으로 추적 가능한 객체여야 하고, 명확한 검증 기준, 제약, 경계, 반복 방식, blocked 정지 조건을 가져야 한다.

- OpenAI Developers Cookbook: https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex
- Codex manual, Goal mode: https://developers.openai.com/codex/codex-manual.md

## 라이선스

MIT
