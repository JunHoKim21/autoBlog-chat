---
name: blogger-publisher
description: >-
  Use this skill when the user asks to summarize, format, and publish conversation content,
  technical concepts, error troubleshooting, or learned terms to Google Blogger (Blogspot).
---

# Blogger Tech Blog Publisher

This skill enables the agent to take any technical discussion, explanation, or code from the current conversation, refine it into a high-quality, professional tech blog post, and automatically publish it to the user's Google Blogger (Blogspot) account via the Blogger API v3.

## When to Trigger
* User requests: "이 내용 블로그에 올려줘", "블로그스팟에 포스팅해줘", "방금 설명한 것 기술 블로그로 발행해줘", "Blogger에 정리해서 올려줘".

## Workflow

### 1. Structure the Content (Markdown)
Refine the conversation context into a structured, production-ready tech blog post:
* **Title**: Clear, engaging, and SEO-friendly (e.g., `[Spring Boot] REQUIRES_NEW 트랜잭션 전파 속성의 동작 원리와 실무 적용 팁`).
* **Tags (Labels)**: 3~5 relevant technical keywords (e.g., `Spring, Transaction, Java, Backend`).
* **Standard Tech Blog Layout**:
  1. **개요 (Overview)**: 핵심 개념 및 한 줄 정의.
  2. **등장 배경 및 필요성 (Why)**: 어떤 문제를 해결하기 위해 고안되었는가?
  3. **동작 원리 및 내부 구조 (How it works)**: 원리, 흐름, 다이어그램(있는 경우).
  4. **실무 코드 예제 (Code Example)**: 프로덕션 수준의 명확하고 간결한 코드.
  5. **실무 주의점 및 트러블슈팅 (Best Practices & Pitfalls)**: 자주 겪는 실수, 성능/동시성 이슈 등.
  6. **한 줄 요약 (Summary)**: 결론.

### 2. Save Temporary Draft File
Save the formatted markdown content into a scratch file:
* File path: `C:\Users\seeroo\.gemini\antigravity\brain\<conversation-id>\scratch\blog_post.md`

### 3. Execute the Publish Script
Run the Python publishing script via `run_command`:

```powershell
python "C:\Users\seeroo\.gemini\config\skills\blogger-publisher\scripts\publish_post.py" --title "게시글 제목" --content-file "임시_마크다운_경로" --labels "태그1,태그2,태그3" --publish
```
*(Note: If the user specifically asks for a draft, replace `--publish` with `--draft`.)*

### 4. Report the Result
Present the published blog post URL directly to the user so they can click and verify it immediately.
