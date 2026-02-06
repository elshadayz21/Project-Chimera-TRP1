import inspect


def test_skills_interface_exports():
    """Assert that skill modules expose the expected callable interfaces as defined in the skills READMEs.

    Expected:
      - skills.content_generator.skill.skill_content_generator(callable)
      - skills.publisher.skill.skill_publisher(callable)
      - skills.trend_fetcher.skill.fetch_trends(callable)
    """

    # Import modules — these modules may exist but the functions should be implemented by the agent.
    from importlib import import_module

    cg_mod = import_module("skills.content_generator")
    pub_mod = import_module("skills.publisher")
    tf_mod = import_module("skills.trend_fetcher")

    # Try to access expected attributes in submodules
    cg_skill = getattr(cg_mod, "skill", None)
    pub_skill = getattr(pub_mod, "skill", None)
    tf_skill = getattr(tf_mod, "skill", None)

    # Expect submodules to expose a callable `skill` object with well-known callables inside.
    assert cg_skill is not None, "skills.content_generator.skill module missing"
    assert pub_skill is not None, "skills.publisher.skill module missing"
    assert tf_skill is not None, "skills.trend_fetcher.skill module missing"

    # Check for functions inside the skill modules (these should be implemented by the agent)
    assert hasattr(cg_skill, "skill_content_generator"), "skill_content_generator not implemented"
    assert inspect.isfunction(getattr(cg_skill, "skill_content_generator"))

    assert hasattr(pub_skill, "skill_publisher"), "skill_publisher not implemented"
    assert inspect.isfunction(getattr(pub_skill, "skill_publisher"))

    assert hasattr(tf_skill, "fetch_trends"), "fetch_trends not implemented"
    assert inspect.isfunction(getattr(tf_skill, "fetch_trends"))
