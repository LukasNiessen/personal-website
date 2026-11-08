```json
{
  "id": "1n1kmcg",
  "author": "trolleid",
  "category": "educational-story",
  "subreddit": "programming",
  "created_utc": 1756309536.0,
  "created_at": "2025-08-27T17:45:36+02:00",
  "permalink": "https://www.reddit.com/r/programming/comments/1n1kmcg/what_are_some_concrete_lessons_youve_learned_in/",
  "link_url": "http://test.com",
  "is_self": false,
  "crosspost_parent": null,
  "removed_by_category": "moderator",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "db5df2c9061103ddbabf288afe2d888b5b86a49c6fd33bef76372ee9819082de",
  "body_sha256": "ad7addba9c9d171aa6649c60e4139edc37d0a89502e2c824e6d1caba460a6354",
  "body_characters": 2519
}
```

# Original title

What are some concrete lessons you’ve learned in your career?

## Original body

I am very curious to hear concrete and valuable lessons you have learned in your career. it’s not so much about lessons that are unknown, but more about how did you learn them, the impact, the story and so on. Here are two examples of my career.

1. In a start up, we were always thinking about adding a CI/CD pipeline to the repository. We knew it’s best practice, we knew it’s going to save time, and we knew that if we actually want to do continuous integration and continuous delivery, then you need a pipe line - triggering tests, building, linting, deployment etc manually with each commit is just not feasible timewise. However, we also knew that setting it up would take a little bit of time, so we always postponed it. Then, one day, we made a manual deployment late night, and the guy responsible got a configuration (a parameter) wrong. Due to that, our users did not have profiles for a few hours, until we released the patch. Lesson learned, it’s not just about saving time, it also prevents mistakes. Of course, this is not a new lesson, there is the famous very similar Knight Capital Group story, but it was a different thing to experience it yourself, as opposed to just reading a story about it online.

2. Again, in the same start-up, for time to market reasons, we skipped tests. We did not write any. We were very well aware, that this is bad practice and that we would have to pay the price of introducing some bugs to production here and there. However we did not know that the tests will not only catch bugs and errors, a test suite also makes your app evolve. And I would argue that it is probably the only way to make your app evolve. When you modify code, that was written a year ago for example, how on earth can you know that you will not break something. You cannot know, because you don’t know all the requirements of the function/…, you don’t know all the dependencies and so on. Even if you have good documentation. So we were always "scared" to touch old code. Lesson learned, there only way to know, and to not be scared, is to have a good and comprehensive test suite in place. Again, this is obviously not a new lesson, some authors such as Michael Feathers or Martin Fowler go as far as even defining legacy code via this, they define legacy code as code that is not well tested. However, also here, experiencing it yourself is a complete different story than reading it in a book.

What stories do you have? Doesn’t need to be technical, can also be about topics such as agile. 

