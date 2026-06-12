from rock_kb.extract import optional_command


def test_optional_tool_lookup_does_not_fail():
    tools = ["crawl4ai", "docling", "markitdown", "repomix", "gitingest", "files-to-prompt", "llm"]
    results = {tool: optional_command(tool) for tool in tools}
    assert set(results) == set(tools)

