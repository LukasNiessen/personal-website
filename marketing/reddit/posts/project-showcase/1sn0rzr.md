```json
{
  "id": "1sn0rzr",
  "author": "trolleid",
  "category": "project-showcase",
  "subreddit": "sre",
  "created_utc": 1776338980.0,
  "created_at": "2026-04-16T13:29:40+02:00",
  "permalink": "https://www.reddit.com/r/sre/comments/1sn0rzr/claude_code_skill_for_terraform_and_opentofu/",
  "link_url": "https://github.com/LukasNiessen/terrashark",
  "is_self": false,
  "crosspost_parent": null,
  "removed_by_category": "moderator",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "2e9d93a98deaa298db485ddc7d5819e60bbf867ce54c77c6a71bacb0fd42727d",
  "body_sha256": "1475e67e001f007de090804393ab71572fc7a8e8466c349c4c5154dc3d8311e8",
  "body_characters": 1037
}
```

# Original title

Claude Code Skill for Terraform and OpenTofu: testing, modules, CI/CD, very token optimized

## Original body

I just shipped a Claude Code & Codex skill that aggregates Terraform Best Practices, largely based on official HashiCorp best practices plus a bunch of other trusted sources I have collected over the years.

There's a couple skills out there already, so let me tell you why I created this skill.

Other skills burned through my tokens. So I checked their reference files and they basically just copied a couple best practice collections + terraform docs and pasted it in md files. Claude reads all of it and it's super expensive.

So I created a different approach. The agent diagnoses most likely failure modes (such as blast radius or secret exposure), and reads only targeted reference files. This is far leaner and far more token efficient, and it works IMO equally well or even better.

Similar to other skills it eliminates LLM hallucinations with Terraform. Curious about feedback!

PS: I also have a 5 min YT video where I demo the skill: [https://www.youtube.com/watch?v=2N1TuxndgpY](https://www.youtube.com/watch?v=2N1TuxndgpY)