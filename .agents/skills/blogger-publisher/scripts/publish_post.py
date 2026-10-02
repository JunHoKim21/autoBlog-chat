import os
import sys
import json
import pickle
import argparse
import markdown
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/blogger']

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
CONFIG_DIR = os.path.join(SKILL_ROOT, 'config')
CLIENT_SECRETS_FILE = os.path.join(CONFIG_DIR, 'client_secrets.json')
TOKEN_FILE = os.path.join(CONFIG_DIR, 'token.pickle')
BLOG_CONFIG_FILE = os.path.join(CONFIG_DIR, 'blog_config.json')

def get_blogger_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token_in:
            creds = pickle.load(token_in)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_FILE, 'wb') as token_out:
                pickle.dump(creds, token_out)
        else:
            raise Exception("유효한 OAuth 토큰이 없습니다. 먼저 auth_and_setup.py를 실행하여 인증을 완료해주세요.")

    return build('blogger', 'v3', credentials=creds)

def main():
    parser = argparse.ArgumentParser(description="Google Blogger 포스팅 도구")
    parser.add_argument("--title", required=True, help="게시글 제목")
    parser.add_argument("--content-file", help="포스팅할 마크다운 파일 경로")
    parser.add_argument("--content", help="포스팅할 마크다운 문자열")
    parser.add_argument("--labels", help="쉼표로 구분된 태그 목록 (예: 'Java,Spring,CS')")
    parser.add_argument("--draft", action="store_true", help="초안(비공개)으로 저장")
    parser.add_argument("--publish", action="store_true", help="즉시 공개로 발행")

    args = parser.parse_args()

    if not os.path.exists(BLOG_CONFIG_FILE):
        raise Exception(f"블로그 설정 파일({BLOG_CONFIG_FILE})이 없습니다. auth_and_setup.py를 먼저 실행하세요.")

    with open(BLOG_CONFIG_FILE, 'r', encoding='utf-8') as f:
        blog_config = json.load(f)

    blog_id = blog_config.get('blog_id')
    if not blog_id:
        raise Exception("blog_config.json에 blog_id가 누락되었습니다.")

    # 1. 마크다운 본문 획득
    md_content = ""
    if args.content_file:
        if not os.path.exists(args.content_file):
            raise FileNotFoundError(f"본문 파일을 찾을 수 없습니다: {args.content_file}")
        with open(args.content_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
    elif args.content:
        md_content = args.content
    else:
        raise ValueError("--content-file 또는 --content 중 하나를 지정해야 합니다.")

    # 2. 마크다운을 깔끔한 HTML로 렌더링
    html_body = markdown.markdown(
        md_content,
        extensions=['fenced_code', 'tables', 'nl2br', 'sane_lists']
    )

    # 블로그 본문용 간단한 스타일 래퍼 (가독성 향상)
    styled_html = f"""<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.7; font-size: 16px; color: #24292e;">
{html_body}
</div>"""

    # 3. 태그 파싱
    labels = []
    if args.labels:
        labels = [lbl.strip() for lbl in args.labels.split(',') if lbl.strip()]

    # 4. 공개 / 초안 여부 결정
    is_draft = blog_config.get('default_is_draft', False)
    if args.draft:
        is_draft = True
    elif args.publish:
        is_draft = False

    # 5. Blogger API 호출
    service = get_blogger_service()
    post_body = {
        'title': args.title,
        'content': styled_html,
        'labels': labels
    }

    result = service.posts().insert(
        blogId=blog_id,
        body=post_body,
        isDraft=is_draft
    ).execute()

    # 결과 출력
    output = {
        "status": "success",
        "post_id": result.get('id'),
        "title": result.get('title'),
        "url": result.get('url'),
        "is_draft": is_draft,
        "labels": result.get('labels', [])
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
