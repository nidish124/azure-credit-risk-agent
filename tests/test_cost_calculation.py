from infra.token_tracker import TokenTracker

def test_cost_calculation():
    tracker = TokenTracker()

    tracker.record_llm_usage(
        agent_name="risk_agent",
        model="gpt-4o-mini",
        prompt_tokens=500,
        completion_tokens=200,
    )

    total = tracker.total_cost()
    assert total > 0
    assert round(total, 6) == round(
        (500/1000)*0.00015 + (200/1000)*0.00060,
        6
    )
