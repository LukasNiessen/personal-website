---
title: 'MVC vs MVP vs MVVM: Choose Your Pattern'
summary: 'Comparing the three main UI architecture patterns. How they work, when to use each one, and practical TypeScript examples.'
date: 'Apr 15 2024'
draft: false
repoUrl: ''
xLink: ''
linkedInLink: ''
tags:
  - Software Architecture
  - Design Patterns
  - UI Development
  - Frontend
  - MVC
  - MVP
  - MVVM
---

# MVC vs MVP vs MVVM: Choose Your Pattern

All three patterns try to separate UI from business logic. They just do it differently.

Let's see how each works and when to use them.

## Model-View-Controller (MVC)

The classic pattern. Controller handles user input, updates Model, View shows data.

```typescript
// Model: Just data and business logic
class UserModel {
  private name: string;
  private email: string;

  updateProfile(data: { name?: string; email?: string }) {
    if (data.name) this.name = data.name;
    if (data.email) this.email = data.email;
    // Validate, save to backend, etc.
  }
}

// View: Shows data, sends user actions to controller
class UserView {
  display(user: { name: string; email: string }) {
    document.getElementById('name').textContent = user.name;
    document.getElementById('email').textContent = user.email;
  }

  onSaveClick(handler: (data: any) => void) {
    document.getElementById('save').onclick = () => {
      const data = {
        name: (document.getElementById('nameInput') as HTMLInputElement).value,
        email: (document.getElementById('emailInput') as HTMLInputElement).value,
      };
      handler(data);
    };
  }
}

// Controller: Handles user input, updates model
class UserController {
  constructor(
    private model: UserModel,
    private view: UserView
  ) {
    this.view.onSaveClick((data) => this.saveUser(data));
  }

  private saveUser(data: any) {
    this.model.updateProfile(data);
    // Update view with new data
  }
}
```

**When to use MVC:**

- Server-side web apps
- Simple CRUD applications
- When user input flow is straightforward

## Model-View-Presenter (MVP)

Like MVC, but Presenter handles both input and output. View is completely passive.

```typescript
// Model stays the same
class UserModel {
  // ... same as MVC example
}

// View just delegates everything to presenter
interface UserView {
  displayName(name: string): void;
  displayEmail(email: string): void;
  onSaveClick(handler: () => void): void;
  getName(): string;
  getEmail(): string;
}

class UserViewImpl implements UserView {
  displayName(name: string) {
    document.getElementById('name').textContent = name;
  }

  displayEmail(email: string) {
    document.getElementById('email').textContent = email;
  }

  getName(): string {
    return (document.getElementById('nameInput') as HTMLInputElement).value;
  }

  getEmail(): string {
    return (document.getElementById('emailInput') as HTMLInputElement).value;
  }

  onSaveClick(handler: () => void) {
    document.getElementById('save').onclick = handler;
  }
}

// Presenter coordinates everything
class UserPresenter {
  constructor(
    private model: UserModel,
    private view: UserView
  ) {
    this.view.onSaveClick(() => this.saveUser());
  }

  private saveUser() {
    const data = {
      name: this.view.getName(),
      email: this.view.getEmail(),
    };
    this.model.updateProfile(data);
    // Update view with new data
  }
}
```

**When to use MVP:**

- Desktop applications
- Complex forms and input validation
- When you need highly testable UI code

## Model-View-ViewModel (MVVM)

View and ViewModel are connected through data binding. Less code, more declarative.

```typescript
// Model still just handles data
class UserModel {
  // ... same as before
}

// ViewModel exposes observable properties
class UserViewModel {
  private nameSubject = new BehaviorSubject<string>('');
  private emailSubject = new BehaviorSubject<string>('');

  name$ = this.nameSubject.asObservable();
  email$ = this.emailSubject.asObservable();

  constructor(private model: UserModel) {}

  updateName(name: string) {
    this.nameSubject.next(name);
  }

  updateEmail(email: string) {
    this.emailSubject.next(email);
  }

  save() {
    this.model.updateProfile({
      name: this.nameSubject.value,
      email: this.emailSubject.value,
    });
  }
}

// View just binds to ViewModel
// Example using a framework with decorators
@Component({
  template: `
    <div>
      <input [ngModel]="name$ | async" (ngModelChange)="updateName($event)" />
      <input [ngModel]="email$ | async" (ngModelChange)="updateEmail($event)" />
      <button (click)="save()">Save</button>
    </div>
  `,
})
class UserComponent {
  constructor(public viewModel: UserViewModel) {}
}
```

**When to use MVVM:**

- Modern frontend frameworks (Angular, Vue)
- Complex UI with lots of data binding
- When you want automatic UI updates

## Key Differences

### Data Flow

**MVC:**

```
User → Controller → Model → View
```

**MVP:**

```
User → View → Presenter → Model → Presenter → View
```

**MVVM:**

```
User → View ↔ ViewModel ↔ Model
```

### Testing

**MVC** - Controllers are easy to test, Views harder
**MVP** - Everything is testable through View interface
**MVVM** - ViewModels are testable, View testing through bindings

### Framework Support

**MVC:**

- ASP.NET MVC
- Ruby on Rails
- Spring MVC

**MVP:**

- Windows Forms
- Android (sort of)

**MVVM:**

- Angular
- Vue.js
- WPF

## Modern Takes

### 1. **Flux/Redux Pattern**

One-way data flow:

```
Action → Dispatcher → Store → View
```

### 2. **Clean Architecture with Use Cases**

```typescript
interface ProfileUseCase {
  updateProfile(data: ProfileData): Promise<void>;
  getProfile(): Promise<Profile>;
}

// Can work with any UI pattern
class ProfilePresenter {
  constructor(private useCase: ProfileUseCase) {}
}
```

### 3. **Component-Based Architecture**

Self-contained components with their own MV\* pattern:

```typescript
@Component({
  selector: 'user-profile',
  template: `...`,
  providers: [UserViewModel],
})
class UserProfileComponent {
  // Combines View and ViewModel in one unit
}
```

## Making the Choice

**Choose MVC when:**

- Building server-side apps
- Need simple, proven pattern
- Have clear separation of input/output

**Choose MVP when:**

- Need highly testable UI code
- Have complex view logic
- Want complete control over the view

**Choose MVVM when:**

- Using modern frontend framework
- Want automatic UI updates
- Have lots of data binding

## Common Mistakes

### 1. **Fat Models**

Don't put everything in the Model:

```typescript
// Bad
class UserModel {
  validateEmail() {}
  formatName() {}
  calculateAge() {}
  // Too many responsibilities
}

// Good
class User {
  // Just data and essential business rules
}
class UserValidator {}
class UserFormatter {}
```

### 2. **Smart Views**

Views should be as dumb as possible:

```typescript
// Bad
class UserView {
  validateAndSave() {
    // View doing too much
  }
}

// Good
class UserView {
  onSaveClick(handler: () => void) {
    // Just delegate to controller/presenter
  }
}
```

### 3. **Tight Coupling**

Use interfaces and dependency injection:

```typescript
interface UserView {
  // View contract
}

class UserPresenter {
  constructor(view: UserView) {
    // Can work with any view implementation
  }
}
```

## Bottom Line

All patterns solve the same problem: separating UI from business logic.

- **MVC** is simple but less testable
- **MVP** is testable but verbose
- **MVVM** is powerful but needs framework support

Pick based on:

1. Your framework
2. Testing needs
3. Team experience

Start simple (MVC), add complexity (MVP/MVVM) when needed.
