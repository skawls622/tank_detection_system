# CCTV Security System

지능형 실시간 기동무기 체계 탐지 및 피아 식별 시스템

## 설치 및 실행

### 1. 프로젝트 클론 또는 다운로드

이 프로젝트를 원하는 폴더에 다운로드하거나 복사합니다.

### 2. 의존성 설치

터미널을 열고 프로젝트 루트 디렉토리에서 다음 명령어를 실행합니다:

```bash
# npm 사용
npm install

# 또는 yarn 사용
yarn install

# 또는 pnpm 사용
pnpm install
```

### 3. 개발 서버 실행

```bash
# npm 사용
npm run dev

# 또는 yarn 사용
yarn dev

# 또는 pnpm 사용
pnpm dev
```

개발 서버가 실행되면 브라우저에서 `http://localhost:5173`으로 접속할 수 있습니다.

### 4. 빌드

프로덕션용 빌드를 생성하려면:

```bash
# npm 사용
npm run build

# 또는 yarn 사용
yarn build

# 또는 pnpm 사용
pnpm build
```

## 프로젝트 구조

```
├── App.tsx                 # 메인 애플리케이션 컴포넌트
├── main.tsx               # React 앱 엔트리 포인트
├── index.html             # HTML 템플릿
├── components/
│   ├── MainLanding.tsx    # 메인 랜딩 페이지
│   ├── AuthPage.tsx       # 로그인/회원가입 페이지
│   └── ui/                # shadcn/ui 컴포넌트들
├── styles/
│   └── globals.css        # 글로벌 CSS 스타일
└── lib/
    └── utils.ts           # 유틸리티 함수들
```

## 커스터마이징

### 배경 영상 변경

`components/MainLanding.tsx` 파일의 `config.background.videoUrl`을 수정하여 배경 영상을 변경할 수 있습니다.

### 텍스트 변경

`components/MainLanding.tsx` 파일의 `config` 객체에서 제목, 부제목, 버튼 텍스트 등을 쉽게 변경할 수 있습니다.

### 로고 변경

`config.logo.icon`에서 lucide-react 아이콘을 변경할 수 있습니다.

## 기술 스택

- **React 18** - UI 라이브러리
- **TypeScript** - 타입 안정성
- **Vite** - 빌드 도구
- **Tailwind CSS v4** - 스타일링
- **shadcn/ui** - UI 컴포넌트 라이브러리
- **lucide-react** - 아이콘 라이브러리

## 지원

문의사항이나 버그 리포트는 프로젝트 관리자에게 연락하세요.