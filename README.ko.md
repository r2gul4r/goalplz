<p align="right">
  <a href="./README.md">English</a> | 한국어
</p>

# Goalplz

Goalplz는 거친 요청을 검증 가능한 Codex Goal mode 목표로 바꿔주는 Codex 플러그인이다.

재사용 가능한 `$goalplz` 스킬과 선택 설치 가능한 `/goalplz` custom prompt alias를 함께 제공한다.

## 왜 필요한가

Codex Goal mode는 목표에 구체적인 결과, 검증면, 제약, 경계, 반복 정책, blocked 정지 조건이 있을 때 가장 잘 작동한다. Goalplz는 애매한 다단계 요청을 Codex가 작업을 시작하기 전에 그 형태로 다시 쓴다.

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

- Goal mode가 맞는 도구인지 판단한다.
- 거친 요청을 검증 가능한 완료 계약으로 변환한다.
- 결과, 검증면, 제약, 경계, 반복 정책, blocked 정지 조건을 잡는다.
- 현재 Codex 표면에서 goal-management 도구를 지원하면 goal을 시작한다.
- 직접 goal 생성이 불가능하면 바로 붙여 넣을 수 있는 `/goal ...` 명령으로 fallback한다.

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

저장소 루트에서 실행:

```bash
codex plugin marketplace add .
```

그 다음 Codex를 재시작하고 `Goalplz Local` marketplace에서 `goalplz`를 설치한다.

수동 local marketplace 방식에서는 Codex가 이 파일을 읽는다:

```text
.agents/plugins/marketplace.json
```

그 marketplace는 이 플러그인을 가리킨다:

```text
./plugins/goalplz
```

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
