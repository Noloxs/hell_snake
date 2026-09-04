# Releasing a New Version

This document outlines the process for creating a new release of Hell Snake. The project uses an automated GitHub Actions workflow to build and publish releases.

## Release Process

To create a new release, follow these steps:

1.  **Ensure `main` is Ready:** Make sure the `main` branch is stable, up-to-date with all desired changes, and that all tests in the CI pipeline are passing.
2.  **Create a Version Tag:** Create a new Git tag that follows semantic versioning (e.g., `vX.Y.Z`). The tag **must** be prefixed with a `v`.

    ```sh
    # Example for version 1.2.3
    git tag v1.2.3
    ```

3.  **Push the Tag:** Push the newly created tag to the remote repository.

    ```sh
    # Example for version 1.2.3
    git push origin v1.2.3
    ```

4.  **Automated Release:** Pushing the tag will automatically trigger the `release.yml` workflow. This workflow will:
    *   Download the Windows executable (`hellsnake.exe`) from the CI pipeline that ran against the tagged commit.
    *   Create a new draft GitHub Release.
    *   Attach the executable to the release.
    *   Automatically generate release notes based on the titles of merged pull requests.

## Branching Considerations

### Releases from `main`

As a rule, releases should **only be created from the `main` branch**. This ensures that every release is based on stable, reviewed, and tested code that has been approved for production.

### The "Gotcha" - How the Workflow Triggers

The release workflow is triggered by the presence of the `.github/workflows/release.yml` file within the specific commit that a tag points to. This means:

-   If you tag a commit on the `main` branch (where the workflow file exists), the release process will work as expected.
-   If you tag a commit on a feature branch that *also* contains the `release.yml` file, the workflow will still trigger. While this is technically possible, it should be avoided for official releases. This practice should be reserved for special cases only, such as creating a pre-release for testing purposes.
