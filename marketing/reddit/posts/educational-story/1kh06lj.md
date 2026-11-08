```json
{
  "id": "1kh06lj",
  "author": "trolleid",
  "category": "educational-story",
  "subreddit": "golang",
  "created_utc": 1746631667.0,
  "created_at": "2025-05-07T17:27:47+02:00",
  "permalink": "https://www.reddit.com/r/golang/comments/1kh06lj/what_is_tdd_and_bdd_which_is_better/",
  "link_url": "https://www.reddit.com/r/golang/comments/1kh06lj/what_is_tdd_and_bdd_which_is_better/",
  "is_self": true,
  "crosspost_parent": null,
  "removed_by_category": "moderator",
  "body_state": "intact",
  "eligible_for_voice": true,
  "archive_only": false,
  "reference_use": "historical_voice_only",
  "retrieved_on": "2026-11-08",
  "source": "Reddit authenticated submitted listing",
  "title_sha256": "3aa7f7c112e496dc1258455ef20eb493671468b9338ed7ed91f446ee2c054eac",
  "body_sha256": "5b7df11266cbdd20300df6c34347623268fc09cf48e1a6c19d39822a084b9c01",
  "body_characters": 10024
}
```

# Original title

What is TDD and BDD? Which is better?

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

```go
func TestUsernameValidatorBDD(t *testing.T) {
	v := &validator.UsernameValidator{}

	t.Run("should accept valid usernames", func(t *testing.T) {
		// Examples of valid usernames
		if !v.IsValid("abc") {
			t.Error("Expected 'abc' to be valid")
		}
		if !v.IsValid("user123") {
			t.Error("Expected 'user123' to be valid")
		}
		if !v.IsValid("valid_username") {
			t.Error("Expected 'valid_username' to be valid")
		}
	})

	t.Run("should reject too short usernames", func(t *testing.T) {
		// Examples of too short usernames
		if v.IsValid("") {
			t.Error("Expected empty string to be invalid")
		}
		if v.IsValid("ab") {
			t.Error("Expected 'ab' to be invalid")
		}
	})

	t.Run("should reject too long usernames", func(t *testing.T) {
		// Examples of too long usernames
		if v.IsValid("abcdefghijklmnopqrstuvwxyz") {
			t.Error("Expected long string to be invalid")
		}
	})

	t.Run("should reject usernames with illegal chars", func(t *testing.T) {
		// Examples of usernames with illegal chars
		if v.IsValid("user@name") {
			t.Error("Expected 'user@name' to be invalid")
		}
		if v.IsValid("special$chars") {
			t.Error("Expected 'special$chars' to be invalid")
		}
	})
}
```

UsernameValidator checks if a username is valid (3-20 characters, alphanumeric and \_). It returns true if all checks pass, else false.

How to test this? Well, if we test if the code does what it does, it might look like this:

```go
// MockValidator is a mock implementation of UsernameValidator for testing
type MockValidator struct {
	mock.Mock
	validator.UsernameValidator
}

// IsTooShort mocks the IsTooShort method
func (m *MockValidator) IsTooShort(username string) bool {
	args := m.Called(username)
	return args.Bool(0)
}

// IsTooLong mocks the IsTooLong method
func (m *MockValidator) IsTooLong(username string) bool {
	args := m.Called(username)
	return args.Bool(0)
}

// ContainsIllegalChars mocks the ContainsIllegalChars method
func (m *MockValidator) ContainsIllegalChars(username string) bool {
	args := m.Called(username)
	return args.Bool(0)
}

func TestUsernameValidatorNonBDD(t *testing.T) {
	t.Run("test IsValid implementation details", func(t *testing.T) {
		// Create a mock validator
		mockValidator := new(MockValidator)
		username := "User@123"
		
		// Set expectations
		mockValidator.On("IsTooShort", username).Return(false)
		mockValidator.On("IsTooLong", username).Return(false)
		mockValidator.On("ContainsIllegalChars", username).Return(true)
		
		// Call IsValid
		result := mockValidator.IsValid(username)
		
		// Verify expectations
		mockValidator.AssertExpectations(t)
		
		// Test with a real validator to verify the expected outcomes
		realValidator := &validator.UsernameValidator{}
		if realValidator.IsTooShort(username) {
			t.Error("Expected username not to be too short")
		}
		if realValidator.IsTooLong(username) {
			t.Error("Expected username not to be too long")
		}
		if !realValidator.ContainsIllegalChars(username) {
			t.Error("Expected username to contain illegal characters")
		}
	})
}
```

This is not great. What if we change the logic inside isValidUsername? Let's say we decide to replace `isTooShort()` and `isTooLong()` by a new method `isLengthAllowed()`?

**The test would break**. Because it almost mirros the implementation. Not good. The test is now tightly coupled to the implementation.

In BDD, we just verify the behavior. So, in this case, we just check if we get the wanted outcome:

```go
func TestUsernameValidatorBDD(t *testing.T) {
	v := &validator.UsernameValidator{}

	t.Run("should accept valid usernames", func(t *testing.T) {
		// Examples of valid usernames
		if !v.IsValid("abc") {
			t.Error("Expected 'abc' to be valid")
		}
		if !v.IsValid("user123") {
			t.Error("Expected 'user123' to be valid")
		}
		if !v.IsValid("valid_username") {
			t.Error("Expected 'valid_username' to be valid")
		}
	})

	t.Run("should reject too short usernames", func(t *testing.T) {
		// Examples of too short usernames
		if v.IsValid("") {
			t.Error("Expected empty string to be invalid")
		}
		if v.IsValid("ab") {
			t.Error("Expected 'ab' to be invalid")
		}
	})

	t.Run("should reject too long usernames", func(t *testing.T) {
		// Examples of too long usernames
		if v.IsValid("abcdefghijklmnopqrstuvwxyz") {
			t.Error("Expected long string to be invalid")
		}
	})

	t.Run("should reject usernames with illegal chars", func(t *testing.T) {
		// Examples of usernames with illegal chars
		if v.IsValid("user@name") {
			t.Error("Expected 'user@name' to be invalid")
		}
		if v.IsValid("special$chars") {
			t.Error("Expected 'special$chars' to be invalid")
		}
	})
}
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

## Another Example of BDD

Lastly another example.

Non-BDD:

```java
@Test
public void testHandleMessage() {
    Publisher publisher = new Publisher();
    List<BuilderList> builderLists = publisher.getBuilderLists();
    List<Log> logs = publisher.getLogs();

    Message message = new Message("test");
    publisher.handleMessage(message);

    // Verify build was created
    assertEquals(1, builderLists.size());
    BuilderList lastBuild = getLastBuild(builderLists);
    assertEquals("test", lastBuild.getName());
    assertEquals(2, logs.size());
}
```

With BDD:

```java
@Test
public void shouldGenerateAsyncMessagesFromInterface() {
    Interface messageInterface = Interfaces.createFrom(SimpleMessageService.class);
    PublisherInterface publisher = new PublisherInterface(messageInterface, transport);

    // When we invoke a method on the interface
    SimpleMessageService service = publisher.createPublisher();
    service.sendMessage("Hello");

    // Then a message should be sent through the transport
    verify(transport).send(argThat(message ->
        message.getMethod().equals("sendMessage") &&
        message.getArguments().get(0).equals("Hello")
    ));
}
```