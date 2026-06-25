"""Tests for budget.core."""

from pathlib import Path

from budget.core import (
    add_transaction,
    filter_by_category,
    get_balance,
    load_transactions_from_csv,
    monthly_summary,
)


def test_add_transaction_increases_length() -> None:
    """Adding a transaction should increase the list length by one."""
    transactions = []
    transaction = {
        "date": "2026-01-07",
        "type": "수입",
        "category": "급여",
        "description": "월급",
        "amount": 3500000,
        "memo": "1월급여",
    }

    result = add_transaction(transactions, transaction)

    assert len(result) == 1
    assert result[0] == transaction


def test_add_transaction_preserves_negative_amount_expense() -> None:
    """Expense transactions with negative amounts should be stored as-is."""
    transactions = []
    transaction = {
        "date": "2026-01-05",
        "type": "지출",
        "category": "식비",
        "description": "점심식사",
        "amount": -12000,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert len(result) == 1
    assert result[0]["amount"] == -12000
    assert result[0]["type"] == "지출"


def test_add_transaction_preserves_positive_amount_income() -> None:
    """Income transactions with positive amounts should be stored as-is."""
    transactions = []
    transaction = {
        "date": "2026-01-28",
        "type": "기타수입",
        "category": "기타수입",
        "description": "중고 판매",
        "amount": 25000,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert len(result) == 1
    assert result[0] == transaction


def test_add_transaction_allows_empty_description() -> None:
    """Empty descriptions should be accepted and stored unchanged."""
    transactions = []
    transaction = {
        "date": "2026-01-10",
        "type": "지출",
        "category": "교통",
        "description": "",
        "amount": -1500,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert len(result) == 1
    assert result[0]["description"] == ""


def test_get_balance_returns_sum_of_transactions() -> None:
    """The balance should equal the sum of all signed transaction amounts."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        },
        {
            "date": "2026-01-15",
            "type": "수입",
            "category": "기타수입",
            "description": "중고 판매",
            "amount": 135541,
            "memo": "",
        },
        {
            "date": "2026-02-13",
            "type": "수입",
            "category": "급여",
            "description": "보너스",
            "amount": 3542940,
            "memo": "",
        },
    ]

    assert get_balance(transactions) == 2698685


def test_get_balance_returns_zero_for_empty_list() -> None:
    """An empty transaction list should have a zero balance."""
    assert get_balance([]) == 0.0


def test_get_balance_matches_step2_csv_total() -> None:
    """The step2 CSV data should produce the expected total balance."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        },
        {
            "date": "2026-01-05",
            "type": "지출",
            "category": "의료",
            "description": "한의원",
            "amount": -65990,
            "memo": "카드결제",
        },
        {
            "date": "2026-01-09",
            "type": "지출",
            "category": "의료",
            "description": "병원 진료",
            "amount": -80861,
            "memo": "",
        },
        {
            "date": "2026-01-10",
            "type": "지출",
            "category": "문화/여가",
            "description": "게임 아이템",
            "amount": -75010,
            "memo": "",
        },
        {
            "date": "2026-01-10",
            "type": "지출",
            "category": "통신",
            "description": "인터넷 요금",
            "amount": -107684,
            "memo": "",
        },
        {
            "date": "2026-01-13",
            "type": "지출",
            "category": "쇼핑",
            "description": "생활용품",
            "amount": -326526,
            "memo": "",
        },
        {
            "date": "2026-01-13",
            "type": "지출",
            "category": "교육",
            "description": "온라인 강의",
            "amount": -432554,
            "memo": "",
        },
        {
            "date": "2026-01-14",
            "type": "지출",
            "category": "여행",
            "description": "여행 경비",
            "amount": -282323,
            "memo": "메모_1",
        },
        {
            "date": "2026-01-15",
            "type": "지출",
            "category": "여행",
            "description": "여행 경비",
            "amount": -659572,
            "memo": "",
        },
        {
            "date": "2026-01-15",
            "type": "지출",
            "category": "문화/여가",
            "description": "영화관",
            "amount": -64470,
            "memo": "현금",
        },
        {
            "date": "2026-01-15",
            "type": "수입",
            "category": "기타수입",
            "description": "중고 판매",
            "amount": 135541,
            "memo": "",
        },
        {
            "date": "2026-01-16",
            "type": "지출",
            "category": "교통",
            "description": "지하철",
            "amount": -90127,
            "memo": "카드결제",
        },
        {
            "date": "2026-01-17",
            "type": "지출",
            "category": "교육",
            "description": "교재 구입",
            "amount": -223148,
            "memo": "카드결제",
        },
        {
            "date": "2026-01-20",
            "type": "지출",
            "category": "의료",
            "description": "한의원",
            "amount": -20331,
            "memo": "현금",
        },
        {
            "date": "2026-01-21",
            "type": "지출",
            "category": "통신",
            "description": "케이블TV",
            "amount": -103886,
            "memo": "카드결제",
        },
        {
            "date": "2026-01-21",
            "type": "지출",
            "category": "주거",
            "description": "가스비",
            "amount": -63306,
            "memo": "메모_20",
        },
        {
            "date": "2026-01-29",
            "type": "지출",
            "category": "식비",
            "description": "편의점",
            "amount": -33021,
            "memo": "",
        },
        {
            "date": "2026-02-01",
            "type": "지출",
            "category": "여행",
            "description": "여행 경비",
            "amount": -651009,
            "memo": "카드결제",
        },
        {
            "date": "2026-02-01",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 4358625,
            "memo": "",
        },
        {
            "date": "2026-02-03",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 4629371,
            "memo": "현금",
        },
        {
            "date": "2026-02-05",
            "type": "지출",
            "category": "쇼핑",
            "description": "옷 구입",
            "amount": -63587,
            "memo": "메모_5",
        },
        {
            "date": "2026-02-08",
            "type": "수입",
            "category": "급여",
            "description": "프리랜서 수입",
            "amount": 3141054,
            "memo": "",
        },
        {
            "date": "2026-02-09",
            "type": "지출",
            "category": "쇼핑",
            "description": "화장품",
            "amount": -239690,
            "memo": "메모_31",
        },
        {
            "date": "2026-02-13",
            "type": "수입",
            "category": "급여",
            "description": "보너스",
            "amount": 3542940,
            "memo": "",
        },
        {
            "date": "2026-02-15",
            "type": "지출",
            "category": "통신",
            "description": "케이블TV",
            "amount": -111988,
            "memo": "현금",
        },
        {
            "date": "2026-02-18",
            "type": "지출",
            "category": "주거",
            "description": "가스비",
            "amount": -169042,
            "memo": "",
        },
        {
            "date": "2026-02-21",
            "type": "지출",
            "category": "의료",
            "description": "치과",
            "amount": -153682,
            "memo": "",
        },
        {
            "date": "2026-02-22",
            "type": "지출",
            "category": "의료",
            "description": "병원 진료",
            "amount": -110130,
            "memo": "",
        },
        {
            "date": "2026-02-24",
            "type": "수입",
            "category": "기타수입",
            "description": "중고 판매",
            "amount": 199790,
            "memo": "",
        },
        {
            "date": "2026-02-24",
            "type": "지출",
            "category": "여행",
            "description": "여행 경비",
            "amount": -1488044,
            "memo": "메모_46",
        },
        {
            "date": "2026-02-25",
            "type": "지출",
            "category": "주거",
            "description": "관리비",
            "amount": -274855,
            "memo": "현금",
        },
        {
            "date": "2026-02-28",
            "type": "지출",
            "category": "주거",
            "description": "인터넷 설치",
            "amount": -71313,
            "memo": "",
        },
        {
            "date": "2026-03-02",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 2895631,
            "memo": "현금",
        },
        {
            "date": "2026-03-03",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -430160,
            "memo": "카드결제",
        },
        {
            "date": "2026-03-07",
            "type": "지출",
            "category": "식비",
            "description": "카페",
            "amount": -17371,
            "memo": "현금",
        },
        {
            "date": "2026-03-10",
            "type": "지출",
            "category": "주거",
            "description": "수도세",
            "amount": -126200,
            "memo": "메모_41",
        },
        {
            "date": "2026-03-11",
            "type": "수입",
            "category": "급여",
            "description": "이자 수입",
            "amount": 3859609,
            "memo": "",
        },
        {
            "date": "2026-03-11",
            "type": "지출",
            "category": "저축/투자",
            "description": "펀드 투자",
            "amount": -654201,
            "memo": "",
        },
        {
            "date": "2026-03-11",
            "type": "지출",
            "category": "쇼핑",
            "description": "옷 구입",
            "amount": -39971,
            "memo": "카드결제",
        },
        {
            "date": "2026-03-12",
            "type": "지출",
            "category": "의료",
            "description": "병원 진료",
            "amount": -6885,
            "memo": "현금",
        },
        {
            "date": "2026-03-14",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 4538391,
            "memo": "카드결제",
        },
        {
            "date": "2026-03-17",
            "type": "지출",
            "category": "식비",
            "description": "분식집",
            "amount": -23926,
            "memo": "",
        },
        {
            "date": "2026-03-18",
            "type": "수입",
            "category": "기타수입",
            "description": "중고 판매",
            "amount": 300049,
            "memo": "현금",
        },
        {
            "date": "2026-03-19",
            "type": "지출",
            "category": "의료",
            "description": "약국",
            "amount": -146373,
            "memo": "현금",
        },
        {
            "date": "2026-03-22",
            "type": "지출",
            "category": "쇼핑",
            "description": "신발 구입",
            "amount": -312698,
            "memo": "현금",
        },
        {
            "date": "2026-03-22",
            "type": "지출",
            "category": "교통",
            "description": "고속도로 통행료",
            "amount": -9734,
            "memo": "",
        },
        {
            "date": "2026-03-23",
            "type": "지출",
            "category": "통신",
            "description": "휴대폰 요금",
            "amount": -52098,
            "memo": "",
        },
        {
            "date": "2026-03-25",
            "type": "지출",
            "category": "교육",
            "description": "교재 구입",
            "amount": -199811,
            "memo": "",
        },
        {
            "date": "2026-03-25",
            "type": "수입",
            "category": "급여",
            "description": "이자 수입",
            "amount": 2754227,
            "memo": "현금",
        },
        {
            "date": "2026-03-25",
            "type": "수입",
            "category": "급여",
            "description": "보너스",
            "amount": 2891172,
            "memo": "",
        },
    ]

    assert get_balance(transactions) == 24285027


def test_filter_by_category_matches_case_insensitively() -> None:
    """Category matching should ignore case and return matching rows only."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        },
        {
            "date": "2026-01-14",
            "type": "지출",
            "category": "여행",
            "description": "여행 경비",
            "amount": -282323,
            "memo": "메모_1",
        },
        {
            "date": "2026-01-15",
            "type": "수입",
            "category": "기타수입",
            "description": "중고 판매",
            "amount": 135541,
            "memo": "",
        },
    ]

    result = filter_by_category(transactions, "여행")

    assert len(result) == 2
    assert all(transaction["category"] == "여행" for transaction in result)

    mixed_case_result = filter_by_category(transactions, "여행".upper())
    assert mixed_case_result == result


def test_filter_by_category_returns_empty_list_for_missing_category() -> None:
    """Unknown categories should return an empty list."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        }
    ]

    assert filter_by_category(transactions, "없는카테고리") == []


def test_filter_by_category_returns_independent_list() -> None:
    """The returned filtered list should not affect the original list."""
    transactions = [
        {
            "date": "2026-01-04",
            "type": "지출",
            "category": "여행",
            "description": "항공권",
            "amount": -979796,
            "memo": "메모_3",
        }
    ]

    result = filter_by_category(transactions, "여행")
    result.append(
        {
            "date": "2026-01-05",
            "type": "수입",
            "category": "여행",
            "description": "추가",
            "amount": 1000,
            "memo": "",
        }
    )

    assert len(transactions) == 1
    assert len(result) == 2


def test_load_transactions_from_csv_reads_step1_file() -> None:
    """CSV loading should read step1 data and convert amount values to ints."""
    csv_path = Path(__file__).resolve().parents[1] / "data" / "step1_transactions.csv"

    transactions = load_transactions_from_csv(csv_path)

    assert len(transactions) == 10
    assert transactions[0] == {
        "date": "2026-01-05",
        "type": "지출",
        "category": "식비",
        "description": "점심식사",
        "amount": -12000,
        "memo": "",
    }
    assert transactions[1]["amount"] == 3500000
    assert isinstance(transactions[1]["amount"], int)
    assert transactions[-1] == {
        "date": "2026-01-28",
        "type": "기타수입",
        "category": "기타수입",
        "description": "중고 판매",
        "amount": 25000,
        "memo": "중고마켓",
    }


def test_monthly_summary_returns_monthly_income_expense_and_net() -> None:
    """Monthly summary should aggregate income, expense, and net by month."""
    csv_path = Path(__file__).resolve().parents[1] / "data" / "step2_transactions.csv"
    transactions = load_transactions_from_csv(csv_path)

    assert monthly_summary(transactions) == {
        "2026-01": {"income": 135541, "expense": -3608605, "net": -3473064},
        "2026-02": {"income": 15871780, "expense": -3333340, "net": 12538440},
        "2026-03": {"income": 17239079, "expense": -2019428, "net": 15219651},
    }


def test_monthly_summary_returns_empty_dict_for_empty_list() -> None:
    """An empty transaction list should return an empty monthly summary."""
    assert monthly_summary([]) == {}
