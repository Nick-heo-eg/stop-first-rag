"""
Boundary Specification Test Suite

These 5 core scenarios MUST pass before every release.
CI MUST fail if any scenario fails.

Core Philosophy (tested in every scenario):
- "Retrieved documents ≠ permission to answer"
- "This system does not automate decisions"
"""

import json
from gate import boundary_gate, DecisionType, StopReason


def test_scenario_1_docs_retrieved_permission_missing():
    """
    Scenario 1: Documents Retrieved + Permission Missing

    Philosophy enforcement:
    "Retrieved documents ≠ permission to answer"

    Expected: STOP with PERMISSION_MISSING reason
    """
    print("\n" + "=" * 70)
    print("SCENARIO 1: Documents Retrieved + Permission Missing")
    print("=" * 70)

    decision = boundary_gate(
        retrieved_docs=True,
        permission_to_answer=False,
        is_decision_request=False
    )

    print(f"Decision: {decision.decision.value}")
    print(f"Reason: {decision.reason}")
    print(f"Explanation: {decision.explanation}")
    print(f"Philosophy: {decision.guidance.get('philosophy', 'N/A')}")

    # Assertions
    assert decision.decision == DecisionType.STOP, \
        "FAIL: Should STOP when permission missing"
    assert decision.reason == StopReason.PERMISSION_MISSING.value, \
        f"FAIL: Expected STOP.PERMISSION_MISSING, got {decision.reason}"
    assert decision.next_actions is not None, \
        "FAIL: STOP must provide next_actions guidance"
    assert "Retrieved documents ≠ permission to answer" in str(decision.guidance), \
        "FAIL: Philosophy statement must be present"

    print("✅ PASS: Correctly blocked generation despite document retrieval")
    return True


def test_scenario_2_no_docs_permission_granted():
    """
    Scenario 2: No Documents + Permission Granted

    Even with permission, cannot answer without evidence.

    Expected: STOP with EVIDENCE_MISSING reason
    """
    print("\n" + "=" * 70)
    print("SCENARIO 2: No Documents + Permission Granted")
    print("=" * 70)

    decision = boundary_gate(
        retrieved_docs=False,
        permission_to_answer=True,
        is_decision_request=False
    )

    print(f"Decision: {decision.decision.value}")
    print(f"Reason: {decision.reason}")
    print(f"Explanation: {decision.explanation}")

    # Assertions
    assert decision.decision == DecisionType.STOP, \
        "FAIL: Should STOP when evidence missing"
    assert decision.reason == StopReason.EVIDENCE_MISSING.value, \
        f"FAIL: Expected STOP.EVIDENCE_MISSING, got {decision.reason}"
    assert decision.next_actions is not None, \
        "FAIL: STOP must provide next_actions guidance"

    print("✅ PASS: Correctly blocked generation when evidence missing")
    return True


def test_scenario_3_decision_request():
    """
    Scenario 3: Decision Request

    Philosophy enforcement:
    "This system does not automate decisions"

    Expected: STOP with DECISION_AUTOMATION_BLOCKED reason
    """
    print("\n" + "=" * 70)
    print("SCENARIO 3: Decision Request")
    print("=" * 70)

    decision = boundary_gate(
        retrieved_docs=True,
        permission_to_answer=True,
        is_decision_request=True
    )

    print(f"Decision: {decision.decision.value}")
    print(f"Reason: {decision.reason}")
    print(f"Explanation: {decision.explanation}")
    print(f"Philosophy: {decision.guidance.get('philosophy', 'N/A')}")

    # Assertions
    assert decision.decision == DecisionType.STOP, \
        "FAIL: Should STOP on decision requests"
    assert decision.reason == StopReason.DECISION_AUTOMATION_BLOCKED.value, \
        f"FAIL: Expected STOP.DECISION_AUTOMATION_BLOCKED, got {decision.reason}"
    assert "This system does not automate decisions" in decision.explanation or \
           "This system does not automate decisions" in str(decision.guidance), \
        "FAIL: Philosophy statement must be present"

    print("✅ PASS: Correctly blocked decision automation")
    return True


def test_scenario_4_adapter_forces_answer():
    """
    Scenario 4: Adapter Attempts to Force ANSWER

    Philosophy > Adapter logic
    Even if adapter suggests ANSWER, STOP if permission missing.

    Expected: STOP (philosophy overrides adapter)
    """
    print("\n" + "=" * 70)
    print("SCENARIO 4: Adapter Attempts to Force ANSWER")
    print("=" * 70)

    decision = boundary_gate(
        retrieved_docs=True,
        permission_to_answer=False,
        is_decision_request=False,
        adapter_suggestion=DecisionType.ALLOW  # Adapter wants to answer
    )

    print(f"Decision: {decision.decision.value}")
    print(f"Reason: {decision.reason}")
    print(f"Explanation: {decision.explanation}")
    print(f"Note: Adapter suggestion was ALLOW, but philosophy enforced STOP")

    # Assertions
    assert decision.decision == DecisionType.STOP, \
        "FAIL: Philosophy must override adapter suggestion"
    assert decision.reason == StopReason.PERMISSION_MISSING.value, \
        f"FAIL: Expected STOP.PERMISSION_MISSING, got {decision.reason}"

    print("✅ PASS: Philosophy correctly overrode adapter suggestion")
    return True


def test_scenario_5_adapter_suggests_stop():
    """
    Scenario 5: Adapter Suggests STOP (but conditions allow)

    Adapter suggestion is advisory only.
    If boundary conditions allow, we proceed with ALLOW.

    Expected: ALLOW (conditions satisfied, adapter is advisory)
    """
    print("\n" + "=" * 70)
    print("SCENARIO 5: Adapter Suggests STOP (but conditions allow)")
    print("=" * 70)

    decision = boundary_gate(
        retrieved_docs=True,
        permission_to_answer=True,
        is_decision_request=False,
        adapter_suggestion=DecisionType.STOP  # Adapter suggests STOP
    )

    print(f"Decision: {decision.decision.value}")
    print(f"Reason: {decision.reason}")
    print(f"Explanation: {decision.explanation}")
    print(f"Note: Adapter suggested STOP, but boundary conditions allow ANSWER")

    # Assertions
    assert decision.decision == DecisionType.ALLOW, \
        "FAIL: Should ALLOW when boundary conditions satisfied"
    assert "Adapter" in decision.explanation, \
        "FAIL: Should acknowledge adapter suggestion was overridden"

    print("✅ PASS: Correctly allowed answer despite adapter suggestion")
    return True


def run_all_tests():
    """
    Run all 5 core scenarios.

    These tests MUST pass in CI before every release.
    """
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "BOUNDARY SPECIFICATION TEST SUITE" + " " * 20 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    print("Core Philosophy:")
    print('  - "Retrieved documents ≠ permission to answer"')
    print('  - "This system does not automate decisions"')
    print()

    tests = [
        ("Scenario 1: Docs+NoPermission", test_scenario_1_docs_retrieved_permission_missing),
        ("Scenario 2: NoDocs+Permission", test_scenario_2_no_docs_permission_granted),
        ("Scenario 3: DecisionRequest", test_scenario_3_decision_request),
        ("Scenario 4: AdapterForcesAnswer", test_scenario_4_adapter_forces_answer),
        ("Scenario 5: AdapterSuggestsStop", test_scenario_5_adapter_suggests_stop),
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except AssertionError as e:
            print(f"❌ FAIL: {e}")
            results.append((name, False))
        except Exception as e:
            print(f"❌ ERROR: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")

    print()
    print(f"Results: {passed}/{total} scenarios passed")

    if passed == total:
        print("\n✅ ALL TESTS PASSED - BOUNDARY SPEC VALIDATED")
        print()
        print("Philosophy enforced:")
        print('  ✅ "Retrieved documents ≠ permission to answer"')
        print('  ✅ "This system does not automate decisions"')
        print()
        return 0  # Success exit code for CI
    else:
        print("\n❌ TESTS FAILED - BOUNDARY SPEC VIOLATED")
        print("\nCI MUST FAIL - DO NOT RELEASE")
        return 1  # Failure exit code for CI


def generate_test_report():
    """
    Generate test report for CI artifact.

    This report should be archived with every CI build.
    """
    report = {
        "test_suite": "Boundary Specification Core Scenarios",
        "philosophy": [
            "Retrieved documents ≠ permission to answer",
            "This system does not automate decisions"
        ],
        "scenarios": [
            {
                "id": 1,
                "name": "Documents Retrieved + Permission Missing",
                "expected": "STOP.PERMISSION_MISSING"
            },
            {
                "id": 2,
                "name": "No Documents + Permission Granted",
                "expected": "STOP.EVIDENCE_MISSING"
            },
            {
                "id": 3,
                "name": "Decision Request",
                "expected": "STOP.DECISION_AUTOMATION_BLOCKED"
            },
            {
                "id": 4,
                "name": "Adapter Forces ANSWER",
                "expected": "STOP (philosophy overrides adapter)"
            },
            {
                "id": 5,
                "name": "Adapter Suggests STOP",
                "expected": "ALLOW (adapter is advisory)"
            }
        ]
    }

    with open("test_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\n📄 Test report generated: test_report.json")


if __name__ == "__main__":
    import sys

    # Generate test report
    generate_test_report()

    # Run all tests
    exit_code = run_all_tests()

    # Exit with appropriate code for CI
    sys.exit(exit_code)
