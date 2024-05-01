from fastapi import APIRouter, HTTPException, Query
import httpx
from starlette.responses import RedirectResponse
import os

router = APIRouter()

KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"

# 카카오 로그인 페이지로 리디렉션
@router.get("/login")
def login():
    return RedirectResponse(
        url=f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"
    )

# 인증 코드를 사용해 액세스 토큰 요청
@router.get("/auth")
async def auth(code: str = Query(...)):
    data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "code": code,
        "client_secret": KAKAO_CLIENT_SECRET
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(KAKAO_TOKEN_URL, data=data)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail="카카오 로그인 인증 토큰 발급 실패")
        
        token_data = r.json()
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        
        # 액세스 토큰을 사용하여 사용자 정보 불러오기
        r = await client.get(KAKAO_USER_INFO_URL, headers=headers)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail="카카오 계정 정보 불러오기 실패")
        
        user_data = r.json()
    return {"user_info": user_data}
