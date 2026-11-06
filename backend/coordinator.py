import os

class Coordinator:
    def __init__(self):
        pass

    def run_triage(self, file_path: str) -> dict:
        """
        파일 경로를 전달받아 3대 분석 엔진을 호출하는 총괄 함수 (현재는 더미 구현체)
        """
        filename = os.path.basename(file_path)

        # 엔진 호출 로직 없이 항상 '정상(NORMAL)' 결과를 반환하는 더미 데이터
        dummy_result = {
            "filename": filename,
            "summary": {
                "verdict": "NORMAL",
                "risk_score": 0
            },
            "details": {
                "hash_engine": {
                    "status": "정상",
                    "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
                    "matched": False
                },
                "pe_engine": {
                    "status": "정상",
                    "is_packed": False,
                    "entropy": 5.4,
                    "anomalies": []
                },
                "yara_engine": {
                    "status": "정상",
                    "matched_count": 0,
                    "rules": []
                }
            }
        }

        return dummy_result