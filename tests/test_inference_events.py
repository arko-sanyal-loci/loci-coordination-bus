import pytest

from coordination_bus.bus import AuthorizationError, ProtocolError, SecureEventBus


def bus():
    b = SecureEventBus()
    b.register_agent("b70", "b" * 32, projects={"arc"},
                     operations={"report_inference", "report_telemetry"})
    b.register_agent("remote", "r" * 32, projects={"arc"}, operations={"issue_verdict"})
    return b


def test_telemetry_and_verdict_accepted():
    b = bus()
    b.publish(sender_agent="b70", project_id="arc", event_type="node.telemetry",
              operation="report_telemetry",
              payload={"node": "b70", "vram_used_mb": 20000, "vram_total_mb": 32768,
                       "util_pct": 91, "queue_depth": 2})
    b.publish(sender_agent="remote", project_id="arc", event_type="oversight.verdict",
              operation="issue_verdict",
              payload={"verdict": "patch", "reason": "off-by-one", "cost_usd": 0.04})
    assert [e.event_type for e in b.events("arc")] == ["node.telemetry", "oversight.verdict"]


def test_event_bound_to_operation():
    b = bus()
    b.register_agent("rogue", "x" * 32, projects={"arc"}, operations={"report_telemetry"})
    with pytest.raises(ProtocolError, match="must use operation issue_verdict"):
        b.publish(sender_agent="rogue", project_id="arc", event_type="oversight.verdict",
                  operation="report_telemetry",
                  payload={"verdict": "approve", "reason": "x", "cost_usd": 0})
    with pytest.raises(AuthorizationError):
        b.publish(sender_agent="b70", project_id="arc", event_type="oversight.verdict",
                  operation="issue_verdict",
                  payload={"verdict": "approve", "reason": "x", "cost_usd": 0})


def test_payload_shape_enforced():
    b = bus()
    with pytest.raises(ProtocolError, match="missing"):
        b.publish(sender_agent="b70", project_id="arc", event_type="node.telemetry",
                  operation="report_telemetry", payload={"node": "b70"})
    with pytest.raises(ProtocolError, match="invalid value"):
        b.publish(sender_agent="b70", project_id="arc", event_type="infer.completed",
                  operation="report_inference",
                  payload={"lane": "gpu9", "tokens_in": 1, "tokens_out": 1,
                           "latency_ms": 5, "tests": "passed"})
