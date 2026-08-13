from __future__ import annotations

from pathlib import Path
import unittest

from zju_learning_tools.constants import READ_METHODS
from zju_learning_tools.server import mcp


class StaticBoundaryTests(unittest.IsolatedAsyncioTestCase):
    async def test_tool_surface_contains_no_remote_write_action(self) -> None:
        tools = await mcp.list_tools()
        names = {tool.name for tool in tools}
        self.assertEqual(len(names), 23)
        self.assertIn("zju_download_resource", names)
        for forbidden in ("submit", "answer", "signin", "sign_in", "post", "upload", "delete", "remove", "complete"):
            self.assertFalse(any(forbidden in name for name in names), (forbidden, sorted(names)))

    async def test_tool_schemas_do_not_accept_urls_or_credentials(self) -> None:
        tools = await mcp.list_tools()
        serialized = "\n".join(str(tool.inputSchema).lower() for tool in tools)
        for forbidden in ("password", "cookie", "authorization", "raw_url", "endpoint"):
            self.assertNotIn(forbidden, serialized)
        self.assertEqual(READ_METHODS, frozenset({"GET", "HEAD"}))

    async def test_tools_are_partitioned_across_task_specific_skills(self) -> None:
        plugin_root = Path(__file__).resolve().parents[1]
        skills_root = plugin_root / "skills"
        expected_skills = {
            "zju-auth-session",
            "zju-course-planning",
            "zju-assignment-grades",
            "zju-resource-downloads",
            "zju-assessments-discussions",
            "zju-zhiyun-classroom",
        }
        actual_skills = {path.parent.name for path in skills_root.glob("*/SKILL.md")}
        self.assertEqual(actual_skills, expected_skills)
        self.assertFalse((skills_root / "zju-learning" / "SKILL.md").exists())

        tools = await mcp.list_tools()
        routed: dict[str, list[str]] = {}
        for skill_name in expected_skills:
            body = (skills_root / skill_name / "SKILL.md").read_text(encoding="utf-8")
            for tool in tools:
                if f"`{tool.name}`" in body:
                    routed.setdefault(tool.name, []).append(skill_name)

        self.assertEqual(set(routed), {tool.name for tool in tools})
        self.assertTrue(all(len(owners) == 1 for owners in routed.values()), routed)

    async def test_skill_prompts_name_their_skill(self) -> None:
        skills_root = Path(__file__).resolve().parents[1] / "skills"
        for skill_file in skills_root.glob("*/SKILL.md"):
            skill_name = skill_file.parent.name
            yaml_text = (skill_file.parent / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertIn(f"${skill_name}", yaml_text)


if __name__ == "__main__":
    unittest.main()
