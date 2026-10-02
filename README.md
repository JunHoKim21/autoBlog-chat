# 🚀 AutoBlog-Chat: Antigravity 블로그스팟 자동 포스팅 스킬

업무 중 AI(Antigravity)와 주고받은 기술 질문, 용어 정리, CS 원리, 에러 해결 과정을 대화창에서 한마디로 정제하여 **Google Blogger(블로그스팟)에 표준 기술 블로그 형식으로 자동 발행**해 주는 에이전트 전용 스킬입니다.

---

## 📦 설치 파일 다운로드 및 빠른 설치 (다른 컴퓨터)

다른 컴퓨터(집 PC, 회사 PC, 노트북 등)에서 복잡한 구글 클라우드 설정이나 로그인 없이 **원클릭으로 바로 설치**할 수 있습니다.

### 1. 설치 파일 다운로드
* 저장소 목록에 있는 **[`blogger-publisher-setup.zip`](https://github.com/JunHoKim21/autoBlog-chat/raw/main/blogger-publisher-setup.zip)** 파일을 다운로드합니다.
  *(또는 터미널에서 `git clone https://github.com/JunHoKim21/autoBlog-chat.git` 실행)*

### 2. 설치 방법 (3초 컷)
1. 다운로드받은 **`blogger-publisher-setup.zip`**의 압축을 풉니다.
2. 폴더 안에 있는 **`install.bat`** 파일을 마우스로 **더블 클릭**합니다.
3. 자동으로 아래 작업이 한 번에 진행됩니다:
   * 필수 Python 라이브러리(`google-api-python-client`, `google-auth-oauthlib`, `markdown`) 자동 설치
   * Antigravity 글로벌 스킬 디렉터리(`~/.gemini/config/skills/blogger-publisher/`)로 자동 복사
   * 이미 발급된 구글 OAuth 영구 토큰(`token.pickle`) 및 블로그 설정 자동 적용

> **💡 구글 로그인이나 API 키 발급이 다시 필요한가요?**  
> **아닙니다!** 설치 파일 안에 이미 인증된 영구 갱신 토큰과 블로그(정확한 정보전달) 설정이 포함되어 있으므로, **다른 컴퓨터에서도 브라우저 로그인 창 없이 바로 동작**합니다.

---

## 💻 사용 방법 (Usage)

별도의 프로그램이나 창을 띄울 필요 없이, **Antigravity 대화창 안에서 평소처럼 사용**하시면 됩니다.

### 1단계: 기술 질문 및 답변
업무 중 궁금한 기술, 코드, 에러 메시지를 평소처럼 질문합니다.
> *예: "Spring 트랜잭션 전파 속성 중에 REQUIRES_NEW 동작 원리가 뭐야?"*  
> *예: "Redis 분산 락 구현할 때 Redisson 쓰는 이유가 뭐야?"*

### 2단계: 블로그 업로드 명령
답변을 확인한 뒤 한마디만 입력하세요:
> 📢 **"이 내용 블로그에 올려줘"**  
> *(공개 전에 먼저 확인하고 싶다면: **"초안(비공개)으로 블로그에 올려줘"**)*

### 3단계: 자동 발행 완료
AI가 내용을 표준 기술 블로그 양식(제목, 개요, 등장 배경, 동작 원리, 코드 예시, 주의점, 태그)으로 정제한 뒤, 블로그스팟에 즉시 포스팅하고 **발행된 글 링크(URL)**를 바로 전달해 드립니다.

---

## 🛠️ 기술 사양 및 구성

* **API 연동**: Google Blogger API v3 (공식 REST API)
* **인증 방식**: Google OAuth 2.0 (Refresh Token 기반 영구 자동 갱신)
* **콘텐츠 엔진**: Markdown to HTML 자동 렌더링 + 스타일 래핑
* **스킬 시스템**: Antigravity Custom Skill Architecture (`SKILL.md`)

```text
blogger-publisher/
├── SKILL.md                  # 스킬 트리거 및 기술 블로그 구조화 프롬프트
├── scripts/
│   ├── publish_post.py       # 블로그스팟 API 포스트 등록 엔진
│   └── auth_server.py        # OAuth 토큰 발급 및 수신 서버
└── config/
    ├── blog_config.json      # 기본 연동 블로그 정보 (정확한 정보전달)
    ├── client_secrets.json   # Google Cloud OAuth 클라이언트 정보
    └── token.pickle          # OAuth 2.0 영구 인증 토큰
```
