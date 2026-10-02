import os
import sys
import json
import pickle
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(line_buffering=True)

SCOPES = ['https://www.googleapis.com/auth/blogger']

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
CONFIG_DIR = os.path.join(SKILL_ROOT, 'config')
CLIENT_SECRETS_FILE = os.path.join(CONFIG_DIR, 'client_secrets.json')
TOKEN_FILE = os.path.join(CONFIG_DIR, 'token.pickle')
BLOG_CONFIG_FILE = os.path.join(CONFIG_DIR, 'blog_config.json')

with open(CLIENT_SECRETS_FILE, 'r', encoding='utf-8') as f:
    secret_data = json.load(f)['installed']

CLIENT_ID = secret_data['client_id']
CLIENT_SECRET = secret_data['client_secret']
REDIRECT_URI = "http://localhost:8080/"

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if 'code' in params:
            auth_code = params['code'][0]
            print(f"\n[수신] 승인 코드를 수신했습니다: {auth_code[:15]}...", flush=True)

            # Google Token Endpoint로 직접 교환
            token_resp = requests.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "code": auth_code,
                    "grant_type": "authorization_code",
                    "redirect_uri": REDIRECT_URI
                }
            )

            if token_resp.status_code == 200:
                token_data = token_resp.json()
                creds = Credentials(
                    token=token_data.get('access_token'),
                    refresh_token=token_data.get('refresh_token'),
                    token_uri='https://oauth2.googleapis.com/token',
                    client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    scopes=SCOPES
                )

                # 토큰 저장
                with open(TOKEN_FILE, 'wb') as f:
                    pickle.dump(creds, f)

                # 워크스페이스에도 토큰 복사
                ws_token = r"c:\PROJECT\source\강의\.agents\skills\blogger-publisher\config\token.pickle"
                with open(ws_token, 'wb') as f:
                    pickle.dump(creds, f)

                print("[성공] 토큰 발급 및 저장 완료!", flush=True)

                # 블로그 정보 조회
                try:
                    service = build('blogger', 'v3', credentials=creds)
                    blogs_result = service.blogs().listByUser(userId='default').execute()
                    items = blogs_result.get('items', [])
                    if items:
                        selected = items[0]
                        cfg = {
                            "blog_id": selected.get('id'),
                            "blog_name": selected.get('name'),
                            "blog_url": selected.get('url'),
                            "default_is_draft": False
                        }
                        with open(BLOG_CONFIG_FILE, 'w', encoding='utf-8') as f:
                            json.dump(cfg, f, ensure_ascii=False, indent=2)

                        ws_cfg = r"c:\PROJECT\source\강의\.agents\skills\blogger-publisher\config\blog_config.json"
                        with open(ws_cfg, 'w', encoding='utf-8') as f:
                            json.dump(cfg, f, ensure_ascii=False, indent=2)

                        print(f"[연동 완료] 블로그: {selected.get('name')} (URL: {selected.get('url')})", flush=True)
                except Exception as e:
                    print(f"[블로그 조회 경고] {e}", flush=True)

                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write("""
                <html>
                <body style="font-family:sans-serif; text-align:center; padding-top:50px;">
                    <h1 style="color:#2ea44f;">인증이 성공적으로 완료되었습니다!</h1>
                    <p style="font-size:18px;">블로그스팟 자동 포스팅 스킬 연동이 완료되었습니다.<br/>이제 이 브라우저 창을 닫으셔도 좋습니다.</p>
                </body>
                </html>
                """.encode('utf-8'))
                print("SERVER_FINISH_SUCCESS", flush=True)
                # 종료 플래그 설정
                sys.exit(0)
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(f"토큰 발급 실패: {token_resp.text}".encode('utf-8'))
                print(f"[오류] 토큰 발급 응답: {token_resp.text}", flush=True)
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No code parameter found")

def main():
    auth_params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/blogger",
        "access_type": "offline",
        "prompt": "consent"
    }
    auth_url = f"https://accounts.google.com/o/oauth2/auth?{urllib.parse.urlencode(auth_params)}"
    
    url_file = os.path.join(SCRIPT_DIR, "auth_url.txt")
    with open(url_file, "w", encoding="utf-8") as f:
        f.write(auth_url)

    print("AUTH_URL_READY", flush=True)
    print(auth_url, flush=True)

    server = HTTPServer(('localhost', 8080), OAuthHandler)
    print("8080 포트에서 인증 요청을 대기 중입니다...", flush=True)
    try:
        server.serve_forever()
    except SystemExit:
        print("서버가 인증 완료 후 정상 종료되었습니다.", flush=True)

if __name__ == '__main__':
    main()
