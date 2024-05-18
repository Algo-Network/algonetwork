# Django Project

## Commit Standard

source : https://www.freecodecamp.org/news/how-to-write-better-git-commit-messages/

Conventional Commits
Now that we've covered basic commit structure of a good commit message, I'd like to introduce Conventional Commits to help provide some detail on creating solid commit messages.

At D2iQ, we use Conventional Commit which is a great practice among engineering teams. Conventional Commit is a formatting convention that provides a set of rules to formulate a consistent commit message structure like so:

```
    <type>[optional scope]: <description>

    [optional body]

    [optional footer(s)]

```

The commit type can include the following:

- `feat`: Introduces a new feature with the changes.
- `fix`: Indicates a bug fix has occurred.
- `chore`: Covers changes that are unrelated to a fix or feature and don't modify src or test files, such as updating dependencies.
- `refactor`: Refactors code without fixing a bug or adding a feature.
- `docs`: Updates to documentation such as the README or other markdown files.
- `style`: Changes that do not affect the meaning of the code, often related to code formatting like white-space or missing semi-colons.
- `test`: Includes new or corrected tests.
- `perf`: Indicates performance improvements.
- `ci`: Related to continuous integration.
- `build`: Changes that affect the build system or external dependencies.
- `revert`: Reverts a previous commit.

The commit type subject line should be all lowercase with a character limit to encourage succinct descriptions.

The optional commit body should be used to provide further detail that cannot fit within the character limitations of the subject line description.

It is also a good location to utilize BREAKING CHANGE: `<description>` to note the reason for a breaking change within the commit.

The footer is also optional. We use the footer to link the JIRA story that would be closed with these changes for example: `Closes D2IQ-<JIRA #>`.

Full Conventional Commit Example

```
    fix: fix foo to enable bar

    This fixes the broken behavior of the component by doing xyz.

    BREAKING CHANGE
    Before this fix foo wasn't enabled at all, behavior changes from <old> to <new>

    Closes D2IQ-12345
```

### Commit Message Comparisons

Review the following messages and see how many of the suggested guidelines they check off in each category.

**Good:**

1. `feat: improve performance with lazy load implementation for images`
2. `chore: update npm dependency to latest version`
3. `Fix bug preventing users from submitting the subscribe form`
4. `Update incorrect client phone number within footer body per client request`

**Bad:**

1. `fixed bug on landing page`
2. `Changed style`
3. `oops`
4. `I think I fixed it this time?`
5. _empty commit messages_

Writing good commit messages is an extremely beneficial skill to develop, and it helps you communicate and collaborate with your team. Commits serve as an archive of changes. They can become an ancient manuscript to help us decipher the past, and make reasoned decisions in the future.
