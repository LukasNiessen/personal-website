```json
{
  "id": "1stseha",
  "author": "trolleid",
  "category": "project-showcase",
  "subreddit": "angularjs",
  "created_utc": 1776971626.0,
  "created_at": "2026-04-23T21:13:46+02:00",
  "permalink": "https://www.reddit.com/r/angularjs/comments/1stseha/i_built_an_open_source_archunitstyle_architecture/",
  "link_url": "https://github.com/LukasNiessen/ArchUnitTS",
  "is_self": false,
  "crosspost_parent": null,
  "removed_by_category": "reddit",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "5905cf11a4c0c6ab3b73317b6f6b542ac534917c26784668918b1ad72bbc6997",
  "body_sha256": "99bffa1c71b6991b54e2df816d116f742d8aa19ab277e8f167791064bdffdb6c",
  "body_characters": 1816
}
```

# Original title

I built an open source ArchUnit-style architecture testing library for TypeScript

## Original body

I recently shipped ArchUnitTS, an open source architecture testing library for TypeScript / JavaScript.

There are already some tools in this space, so let me explain why I built another one.

What I wanted was not just import linting or dependency visualization. I wanted actual architecture tests that live in the normal test suite and run in CI, similar in spirit to ArchUnit on the JVM side.

So I built ArchUnitTS.

With it, you can test things like:

- forbidden dependencies between layers
- circular dependencies
- naming conventions
- architecture slices
- UML / PlantUML conformance
- code metrics like cohesion, coupling, instability, etc.
- custom architecture rules if the built-ins are not enough

Simple layered architecture example: 

```
it('presentation layer should not depend on database layer', async () => {
  const rule = projectFiles()
    .inFolder('src/presentation/**')
    .shouldNot()
    .dependOnFiles()
    .inFolder('src/database/**');

  await expect(rule).toPassAsync();
});
```

I wanted it to integrate naturally into existing setups instead of forcing people into a separate workflow. So it works with normal test pipelines and supports frameworks like Jest, Vitest, Jasmine, Mocha, etc.

Maybe a detail, but ane thing that mattered a lot to me is avoiding false confidence. For example, with some architecture-testing approaches, if you make a mistake in a folder pattern, the rule may effectively run against 0 files and still pass. That’s pretty dangerous. ArchUnitTS detects these “empty tests” by default and fails them, which IMO is much safer. Other libraries lack this unfortunately.

Curious about any type of feedback!!

GitHub: https://github.com/LukasNiessen/ArchUnitTS

PS: I also made a 20-minute live coding demo on YT:
https://www.youtube.com/watch?v=-2FqIaDUWMQ