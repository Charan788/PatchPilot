import unittest
from scripts.configure_agent import build, READS, WRITES

class PolicyTests(unittest.TestCase):
    def test_all_writes_gated(self):
        m = build("provider/model", "github")["manifest"]
        c = m["mcp_servers"][0]
        self.assertEqual(set(c["enable_tools"]), set(READS + WRITES))
        self.assertEqual(set(c["require_approval_for_tools"]), set(WRITES))
        self.assertNotIn("merge_pull_request", c["enable_tools"])
        self.assertTrue(m["config"]["sandbox"]["enabled"])
        self.assertFalse(m["config"]["dynamic_sub_agents"]["enabled"])
    def test_empty_model_rejected(self):
        with self.assertRaises(ValueError):
            build("", "github")

