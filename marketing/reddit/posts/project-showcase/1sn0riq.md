```json
{
  "id": "1sn0riq",
  "author": "trolleid",
  "category": "project-showcase",
  "subreddit": "kubernetes",
  "created_utc": 1776338943.0,
  "created_at": "2026-04-16T13:29:03+02:00",
  "permalink": "https://www.reddit.com/r/kubernetes/comments/1sn0riq/claude_code_skill_for_kubernetes_token_optimized/",
  "link_url": "https://github.com/LukasNiessen/kubernetes-skill",
  "is_self": false,
  "crosspost_parent": null,
  "removed_by_category": "moderator",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "f2e9fe251a67dacf48a8f393a85b4eb7c39f86558a32aad993b4ea29a3544c70",
  "body_sha256": "ddfd1d6d66ea54603ff3d3bb8992c7e4e52724401b116c2a20c894e61181e668",
  "body_characters": 779
}
```

# Original title

Claude Code Skill for Kubernetes - token optimized

## Original body

I just shipped a Claude Code & Codex skill that aggregates Kubernetes Best Practices plus a bunch of other trusted sources I have collected over the years.

There's a couple skills out there already, so let me tell you why I created this skill.

Other skills burned through my tokens. So I checked their reference files and they basically just copied a couple best practice collections + docs and pasted it in md files. Claude reads all of it and it's super expensive.

So I created a different approach. The agent diagnoses most likely failure modes, and reads only targeted reference files. This is far leaner and far more token efficient, and it works IMO equally well or even better.

Similar to other skills it eliminates LLM hallucinations with K8s. Curious about feedback!