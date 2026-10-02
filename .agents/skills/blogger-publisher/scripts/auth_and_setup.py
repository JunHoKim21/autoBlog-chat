import os
import sys
import json
import pickle
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# 출력 버퍼링 즉시 플러시 설정
sys.stdout.reconfigure(line_buffering=True)

SCOPES = ['https://www.googleapis.com/auth/blogger']

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
CONFIG_DIR = os.path.join(SKILL_ROOT, 'config')
CLIENT_SECRETS_FILE = os.path.join(CONFIG_DIR, 'client_secrets.json')
TOKEN_FILE = os.path.join(CONFIG_DIR, 'token.pickle')
BLOG_CONFIG_FILE = os.path.join(CONFIG_DIR, 'blog_config.json')

def main():
    if not os.path.exists(CLIENT_SECRETS_FILE):
        print(f"[오류] 클라이언트 시크릿 파일이 없습니다: {CLIENT_SECRETS_FILE}", flush=True)
        sys.exit(1)

    print("Google OAuth 2.0 인증을 시작합니다...", flush=True)

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    
    # run_local_server 실행 (open_browser=False로 두고 URL을 명시적으로 출력 및 OS 기본 브라우저 실행)
    creds = flow.run_local_server(
        host='localhost',
        port=8080,
        authorization_prompt_message="인증을 위해 아래 URL에 접속해주세요:\n{url}",
        success_message="인증이 성공적으로 완료되었습니다! 이 창을 닫고 Antigravity로 돌아가셔도 좋습니다.",
        open_browser=True
    )

    # 토큰 영구 저장
    with open(TOKEN_FILE, 'wb') as token_out:
        pickle.dump(creds, token_out)
    print(f"\n[성공] OAuth 토큰이 안전하게 저장되었습니다: {TOKEN_FILE}", flush=True)

    # Blogger 서비스 생성 및 블로그 목록 자동 조회
    service = build('blogger', 'v3', credentials=creds)
    blogs_result = service.blogs().listByUser(userId='default').execute()
    items = blogs_result.get('items', [])

    if not items:
        print("\n[경고] 연결된 Blogger 블로그를 찾을 수 없습니다.", flush=True)
        print("https://www.blogger.com 에 접속하여 블로그를 최소 1개 생성한 후 다시 실행해주세요.", flush=True)
        sys.exit(1)

    print(f"\n[조회 완료] 발견된 블로그 목록 ({len(items)}개):", flush=True)
    for idx, b in enumerate(items):
        print(f" [{idx + 1}] 이름: {b.get('name')} | ID: {b.get('id')} | URL: {b.get('url')}", flush=True)

    selected = items[0]
    print(f"\n-> 기본 연동 블로그: '{selected.get('name')}' (ID: {selected.get('id')})", flush=True)

    config_data = {
        "blog_id": selected.get('id'),
        "blog_name": selected.get('name'),
        "blog_url": selected.get('url'),
        "default_is_draft": False
    }

    with open(BLOG_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)

    print(f"[설정 완료] 블로그 설정이 저장되었습니다: {BLOG_CONFIG_FILE}", flush=True)
    print("이제 '블로그에 올려줘' 명령으로 바로 포스팅하실 수 있습니다!\n", flush=True)

if __name__ == '__main__':
    main()
