from contracts.policy_output import PolicyEvaluationOutput


def test_policy_pass():
    policy = PolicyEvaluationOutput(
        policy_status="PASS",
        conditions=[],
        hard_stop=False,
        policy_references=["CREDIT-POL-4.1"]
    )

    assert policy.policy_status == "PASS"
    assert policy.hard_stop is False


def test_policy_hard_stop():
    policy = PolicyEvaluationOutput(
        policy_status="FAIL",
        conditions=[],
        hard_stop=True,
        policy_references=["CREDIT-POL-9.3"]
    )

    assert policy.hard_stop is True
