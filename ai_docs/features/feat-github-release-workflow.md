# feat: Automated Release Workflow

This document outlines the plan to create an automated GitHub Actions workflow that publishes a new release, with the compiled executable attached, whenever a version tag is pushed to the repository.

---

## User Story
**As a** developer,
**I want to** automate the creation of a GitHub release when a version tag is pushed,
**so that** the compiled `.exe` artifact is formally published for users to download.

---

## Scope
### In Scope
- A new workflow that triggers when a tag matching `v*.*.*` is pushed.
- The workflow will download the `.exe` artifact from the `ci-pipeline.yml` run corresponding to the commit the tag was pushed from.
- It will then create a GitHub Release using the pushed tag.
- The release body will be automatically generated from pull request titles.
- The downloaded `.exe` will be attached to that release.

### Out of Scope
- Modifying the existing build process in `ci-pipeline.yml`.
- Handling tags that do not match the `v*.*.*` pattern.

---

## Dependencies and Risks
- **Dependency:** The new workflow is dependent on the `build-executable` job in `ci-pipeline.yml` completing successfully.
- **Dependency:** The workflow will use existing, trusted GitHub Actions to (1) download the artifact from the other workflow and (2) create the release.
- **Dependency:** The workflow will require a `GITHUB_TOKEN` with write permissions for releases.
- **Risk:** The primary risk is ensuring the workflow always downloads the artifact from the correct CI run for the tagged commit. This requires careful configuration.
- **Risk:** The quality of the auto-generated release notes will depend on the clarity and consistency of pull request titles.

---

## Relevant Files
- `.github/workflows/release.yml` (to be created)

---

## Implementation Plan
- [x] **Create Workflow File**
  - [x] Create a new file named `release.yml` inside the `.github/workflows/` directory.
- [x] **Define Workflow Trigger**
  - [x] Configure the workflow to trigger on a `push` event for tags matching the `v*.*.*` pattern.
- [x] **Configure Release Job**
  - [x] Define a single job named `release` that runs on `ubuntu-latest`.
  - [x] Grant the job `contents: write` permissions to allow release creation.
- [x] **Implement Job Steps**
  - [x] **Download Artifact:** Add a step using a community action to download the `hellsnake-windows.exe` artifact from the `ci-pipeline.yml` workflow run that was triggered by the same commit.
  - [x] **Create Release:** Add a final step using a community action to draft a new GitHub Release. This step will be configured to:
    - [x] Automatically generate release notes from merged pull requests.
    - [x] Upload the downloaded `hellsnake-windows.exe` as a release asset.

---

## Acceptance Criteria
- When a tag matching `v*.*.*` is pushed, the `release.yml` workflow is triggered.
- The workflow run completes successfully.
- A new GitHub Release is created, with the tag and title matching the pushed tag.
- The release body contains auto-generated content.
- The `hellsnake-windows.exe` file is attached to the release as an artifact.
