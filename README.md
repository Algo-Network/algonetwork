# Django Project

Link Demo Project: [YouTube Video](https://youtu.be/DR_e97_m13I)

## Steps to Run Locally

### 1. Create a Local Image Database (PostgreSQL)

Run the following command to start the Docker service, which will create and configure the PostgreSQL database:

```sh
docker-compose up
```

### 2. Run Tailwind CSS

Run the following command to start the Tailwind CSS development process:

```sh
python manage.py tailwind start
```

### 3. Run Django Web Server

Run the following command to start the Django development server:

```sh
python manage.py runserver
```

### 4. Run Celery

Run the following commands to activate the virtual environment and start Celery:

```sh
cd .\env\Scripts\
.\activate
cd ..\..

celery -A coldemail worker --pool=solo -l info # to run the worker

celery -A coldemail beat -l info # to log check celery
```

---

## Feature Description

## Email Generator (FE + BE)

Ensure migrations have been applied first:

```sh
python manage.py makemigrations
python manage.py migrate
```

This feature allows users to input prompts to generate emails.

---

## Staff Account Registration on Algo Network

### Brief Description

This section explains the process of registering a staff account on the Algo Network application. Only superusers have access to create staff accounts. A staff account allows users to log into the Algo Network web application.

### Staff Account Registration Explanation

1. **Access Registration Page**:

   - Superusers access the registration page (create staff account) on the Algo Network web.
   - The registration page is only accessible to users logged in with a superuser account.

2. **Staff Account Access**:
   - After successful registration, users can use the staff account to log into the Algo Network web.
   - Users can access certain features and functionalities available within the application.

---

## Commit Standards

### Conventional Commits

To ensure clarity and consistency in commit messages, we use Conventional Commits, a formatting convention that provides rules for creating consistent commit message structures as follows:

```
    <type>[optional scope]: <description>

    [optional body]

    [optional footer(s)]
```

#### Commit Types

- `feat`: Introduces a new feature.
- `fix`: Indicates a bug fix.
- `chore`: Covers changes unrelated to a fix or feature, such as updating dependencies.
- `refactor`: Refactors code without fixing a bug or adding a feature.
- `docs`: Updates to documentation.
- `style`: Changes that do not affect the meaning of the code, such as formatting.
- `test`: Includes new or corrected tests.
- `perf`: Indicates performance improvements.
- `ci`: Related to continuous integration.
- `build`: Changes affecting the build system or external dependencies.
- `revert`: Reverts a previous commit.

The subject line should be lowercase and succinct. The body should provide further detail if necessary. Use `BREAKING CHANGE: <description>` for breaking changes, and the footer to link issues or stories.

#### Example

```
    fix: fix foo to enable bar

    This fixes the broken behavior of the component by doing xyz.

    BREAKING CHANGE
    Before this fix, foo wasn't enabled at all. Behavior changes from <old> to <new>.

    Closes D2IQ-12345
```

### Good vs. Bad Commit Messages

**Good:**

1. `feat: improve performance with lazy load implementation for images`
2. `chore: update npm dependency to latest version`
3. `fix: fix bug preventing users from submitting the subscribe form`
4. `docs: update client phone number in footer`

**Bad:**

1. `fixed bug on landing page`
2. `changed style`
3. `oops`
4. `I think I fixed it this time?`
5. _empty commit messages_

Writing good commit messages is crucial for effective communication and collaboration within a team. They serve as an archive of changes, helping us understand the past and make informed decisions in the future.
