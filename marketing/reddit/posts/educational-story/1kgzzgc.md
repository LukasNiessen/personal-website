```json
{
  "id": "1kgzzgc",
  "author": "trolleid",
  "category": "educational-story",
  "subreddit": "Frontend",
  "created_utc": 1746631187.0,
  "created_at": "2025-05-07T17:19:47+02:00",
  "permalink": "https://www.reddit.com/r/Frontend/comments/1kgzzgc/eli5_what_is_tdd_and_bdd_also_tdd_vs_bdd/",
  "link_url": "https://www.reddit.com/r/Frontend/comments/1kgzzgc/eli5_what_is_tdd_and_bdd_also_tdd_vs_bdd/",
  "is_self": true,
  "crosspost_parent": null,
  "removed_by_category": "moderator",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "f55a72f1b3851a4ff3ff81d456762454cf1666f2f60ce7da2c3d6716e2e4533a",
  "body_sha256": "4cc7827d1c2b387a78562ff32cc887dc6df4ae67f15b3d775e4f44b00b121956",
  "body_characters": 7387
}
```

# Original title

ELI5: What is TDD and BDD? Also, TDD vs BDD?

## Original body

I wrote this short article about TDD vs BDD because I couldn't find a concise one. It contains code examples in every common dev language. Maybe it helps one of you :-)
Here is the repo: https://github.com/LukasNiessen/tdd-bdd-explained

# TDD and BDD Explained

_TDD = Test-Driven Development_  
_BDD = Behavior-Driven Development_

## Behavior-Driven Development

BDD is all about the following mindset: **Do not test code. Test behavior.**

So it's a shift of the testing mindset. This is why in BDD, we also introduced new terms:

- **Test suites** become **specifications**,
- **Test cases** become **scenarios**,
- We don't **test code**, we **verify behavior**.

Let's make this clear by an example.

## Java Example

If you are not familiar with Java, look in the repo files for other languages (I've added: Java, Python, JavaScript, C#, Ruby, Go).

```javascript
class UsernameValidator {
  isValid(username) {
    if (this.isTooShort(username)) {
      return false;
    }
    if (this.isTooLong(username)) {
      return false;
    }
    if (this.containsIllegalChars(username)) {
      return false;
    }
    return true;
  }

  isTooShort(username) {
    return username.length < 3;
  }

  isTooLong(username) {
    return username.length > 20;
  }

  // allows only alphanumeric and underscores
  containsIllegalChars(username) {
    return !username.match(/^[a-zA-Z0-9_]+$/);
  }
}
```

UsernameValidator checks if a username is valid (3-20 characters, alphanumeric and \_). It returns true if all checks pass, else false.

How to test this? Well, if we test if the code does what it does, it might look like this:

```javascript
describe("Username Validator Non-BDD Style", () => {
  it("tests isValid method", () => {
    // Create spy/mock
    const validator = new UsernameValidator();
    const isTooShortSpy = sinon.spy(validator, "isTooShort");
    const isTooLongSpy = sinon.spy(validator, "isTooLong");
    const containsIllegalCharsSpy = sinon.spy(
      validator,
      "containsIllegalChars"
    );

    const username = "User@123";
    const result = validator.isValid(username);

    // Check if all methods were called with the right input
    assert(isTooShortSpy.calledWith(username));
    assert(isTooLongSpy.calledWith(username));
    assert(containsIllegalCharsSpy.calledWith(username));

    // Now check if they return the correct results
    assert.strictEqual(validator.isTooShort(username), false);
    assert.strictEqual(validator.isTooLong(username), false);
    assert.strictEqual(validator.containsIllegalChars(username), true);
  });
});
```

This is not great. What if we change the logic inside isValidUsername? Let's say we decide to replace `isTooShort()` and `isTooLong()` by a new method `isLengthAllowed()`?

**The test would break**. Because it almost mirros the implementation. Not good. The test is now tightly coupled to the implementation.

In BDD, we just verify the behavior. So, in this case, we just check if we get the wanted outcome:

```javascript
describe("Username Validator BDD Style", () => {
  let validator;

  beforeEach(() => {
    validator = new UsernameValidator();
  });

  it("should accept valid usernames", () => {
    // Examples of valid usernames
    assert.strictEqual(validator.isValid("abc"), true);
    assert.strictEqual(validator.isValid("user123"), true);
    assert.strictEqual(validator.isValid("valid_username"), true);
  });

  it("should reject too short usernames", () => {
    // Examples of too short usernames
    assert.strictEqual(validator.isValid(""), false);
    assert.strictEqual(validator.isValid("ab"), false);
  });

  it("should reject too long usernames", () => {
    // Examples of too long usernames
    assert.strictEqual(validator.isValid("abcdefghijklmnopqrstuvwxyz"), false);
  });

  it("should reject usernames with illegal chars", () => {
    // Examples of usernames with illegal chars
    assert.strictEqual(validator.isValid("user@name"), false);
    assert.strictEqual(validator.isValid("special$chars"), false);
  });
});
```

Much better. If you change the implementation, the tests will not break. They will work as long as the method works.

Implementation is irrelevant, we only specified our wanted behavior. This is why, in BDD, we don't call it a _test suite_ but we call it a _specification_.

Of course this example is very simplified and doesn't cover all aspects of BDD but it clearly illustrates the core of BDD: **testing code vs verifying behavior**.

## Is it about tools?

Many people think BDD is something written in Gherkin syntax with tools like Cucumber or SpecFlow:

```gherkin
Feature: User login
  Scenario: Successful login
    Given a user with valid credentials
    When the user submits login information
    Then they should be authenticated and redirected to the dashboard
```

While these tools are great and definitely help to implement BDD, it's not limited to them. BDD is much broader. BDD is about behavior, not about tools. You can use BDD with these tools, but also with other tools. Or without tools at all.

## More on BDD

https://www.youtube.com/watch?v=Bq_oz7nCNUA (by Dave Farley)  
https://www.thoughtworks.com/en-de/insights/decoder/b/behavior-driven-development (Thoughtworks)

---

## Test-Driven Development

TDD simply means: Write tests first! Even before writing the any code.

So we write a test for something that was not yet implemented. And yes, of course that test will fail. This may sound odd at first but TDD follows a simple, iterative cycle known as Red-Green-Refactor:

- **Red**: Write a failing test that describes the desired functionality.
- **Green**: Write the minimal code needed to make the test pass.
- **Refactor**: Improve the code (and tests, if needed) while keeping all tests passing, ensuring the design stays clean.

This cycle ensures that every piece of code is justified by a test, reducing bugs and improving confidence in changes.

## Three Laws of TDD

Robert C. Martin (Uncle Bob) formalized TDD with three key rules:

- You are not allowed to write any production code unless it is to make a failing unit test pass.
- You are not allowed to write any more of a unit test than is sufficient to fail; and compilation failures are failures.
- You are not allowed to write any more production code than is sufficient to pass the currently failing unit test.

## TDD in Action

For a practical example, check out this video of Uncle Bob, where he is coding live, using TDD: https://www.youtube.com/watch?v=rdLO7pSVrMY

It takes time and practice to "master TDD".

## Combine them (TDD + BDD)!

TDD and BDD complement each other. It's best to use both.

TDD ensures your code is correct by driving development through failing tests and the Red-Green-Refactor cycle. BDD ensures your tests focus on what the system should do, not how it does it, by emphasizing behavior over implementation.

Write TDD-style tests to drive small, incremental changes (Red-Green-Refactor). Structure those tests with a BDD mindset, specifying behavior in clear, outcome-focused scenarios.
This approach yields code that is:

- Correct: TDD ensures it works through rigorous testing.
- Maintainable: BDD's focus on behavior keeps tests resilient to implementation changes.
- Well-designed: The discipline of writing tests first encourages modularity, loose coupling, and clear separation of concerns.