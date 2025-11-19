# Windows Credential Manager 통합 변경사항

## 개요
마스터 패스워드를 Windows 자격 증명 관리자에 안전하게 저장하여, 매번 패스워드를 입력하지 않아도 되도록 개선했습니다.

## 주요 변경사항

### 1. crypto_utils.py
- `keyring` 라이브러리 추가 (선택적 import)
- 새로운 함수들 추가:
  - `is_keyring_available()`: keyring 사용 가능 여부 확인
  - `save_master_password(password)`: 마스터 패스워드를 Windows 자격 증명 관리자에 저장
  - `load_master_password()`: 저장된 마스터 패스워드 불러오기
  - `delete_master_password()`: 저장된 마스터 패스워드 삭제

### 2. wol_mstsc.py
- `get_master_password()` 함수 개선:
  - 먼저 Windows 자격 증명 관리자에서 저장된 패스워드를 불러옴
  - 저장된 패스워드가 없으면 사용자 입력 요청
  - 새로운 패스워드 입력 시 저장 여부를 물어봄
  
- `delete_saved_master_password()` 함수 추가:
  - 저장된 마스터 패스워드 삭제 기능
  
- `change_master_password()` 함수 개선:
  - 마스터 패스워드 변경 시 자격 증명 관리자의 저장된 패스워드도 자동 업데이트

- Options 메뉴 업데이트:
  - 새 옵션 추가: "6. Delete Saved Master Password from Credential Manager"
  - 기존 옵션들 번호 조정 (1-9)

### 3. requirements.txt
- `keyring>=24.0.0` 의존성 추가

### 4. test_credential_manager.py (신규)
- Windows 자격 증명 관리자 통합 테스트 스크립트
- 저장/불러오기/삭제 기능 검증

## 사용 방법

### 설치
```bash
pip install -r requirements.txt
```

### 최초 실행 시
1. 프로그램 실행 시 마스터 패스워드 입력
2. "💾 Save this password to Windows Credential Manager? (y/n):" 메시지에서 `y` 입력
3. 이후 실행부터는 패스워드 입력 불필요 (자동으로 불러옴)

### 저장된 패스워드 사용
- 프로그램이 자동으로 Windows 자격 증명 관리자에서 패스워드를 불러옵니다
- "🔑 Using saved master password from Windows Credential Manager" 메시지 표시

### 저장된 패스워드 삭제
1. 프로그램 실행 후 Options 메뉴 진입 (Enter 키)
2. 옵션 6 선택: "Delete Saved Master Password from Credential Manager"
3. 확인 후 삭제

### 보안 정보
- 패스워드는 Windows 자격 증명 관리자에 저장됩니다
- 서비스 이름: `WOL-MSTSC`
- 계정 이름: `MasterPassword`
- Windows의 DPAPI를 사용하여 암호화됨
- 다른 Windows 계정에서는 접근 불가능

## 동작 확인
테스트 스크립트 실행:
```bash
python test_credential_manager.py
```

모든 테스트가 통과하면 정상 작동합니다.

## 주의사항
- `keyring` 라이브러리가 설치되지 않은 경우, 기존 방식대로 매번 패스워드 입력 필요
- Windows 자격 증명 관리자는 사용자 계정별로 관리됨
- 마스터 패스워드 변경 시 저장된 패스워드도 자동으로 업데이트됨
