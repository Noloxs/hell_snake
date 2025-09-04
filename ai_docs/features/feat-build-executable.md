# feat: Build Executable

This document outlines the plan to package the Hell Snake Python application into a single, distributable `.exe` file for Windows. This will simplify distribution and allow users to run the application without needing to install Python or any dependencies.

---

## User Stories
**As a** developer,
**I want to** package the application into an `.exe`,
**so that** I can easily distribute it to users.

**As a** developer,
**I want to** automate the build process in a CI/CD pipeline,
**so that** a new executable is automatically created and attached to every release.

---

## Scope
### In Scope
- Create a single, self-contained `.exe` file.
- Bundle all necessary assets (icons, fonts, `stratagems.json`) within the executable.
- Create a GitHub Actions workflow to build the executable and attach it as a release artifact.

### Out of Scope
- Creating an installer (e.g., MSI).
- Code signing the executable.
- Creating builds for operating systems other than Windows.

---

## Dependencies and Risks
- **Dependency:** The project will require the `pyinstaller` library. This will be added to the project's dependencies.
- **Risk:** None identified.

---

## Relevant Files
- `requirements.txt` (to be modified)
- `Makefile` (to be modified)
- `.gitignore` (to be modified)
- `hellsnake.spec` (to be created)
- `.github/workflows/ci-pipeline.yml` (to be created/renamed)

---

## Implementation Plan
### Local Build
- [x] **Dependency Management**
  - [x] Add `pyinstaller` to the `requirements.txt` file.
- [x] **Build Automation**
  - [x] Add a `build` command to the `Makefile` to automate the execution of PyInstaller.
- [x] **Build Configuration**
  - [x] Create a `hellsnake.spec` file to configure the build.
  - [x] Ensure the spec file includes all assets from `src/res/` (icons, fonts, `stratagems.json`).
  - [x] Set the application icon in the spec file.
- [x] **Repository Maintenance**
  - [x] Add PyInstaller-generated directories (`build/`, `dist/`) and files (`*.spec`) to the `.gitignore` file.

### GitHub Actions Workflow
- [x] **Workflow Refactoring**
  - [x] Rename the existing workflow file from `.github/workflows/run_test.yml` to `.github/workflows/ci-pipeline.yml`.
  - [x] Rename the existing `build` job to `test`.
- [x] **Build Job**
  - [x] Add a new job named `build-executable` that runs on `windows-latest`.
  - [x] Configure the job to run only after the `test` job succeeds (`needs: test`).
  - [x] Add a condition to ensure the job only runs for pushes to the `main` branch or on new releases.
  - [x] Add steps to check out code, set up Python, install dependencies, and run `make build`.
- [x] **Artifact Management**
  - [x] Add a step to upload the generated `.exe` as a build artifact.
  - [x] For release triggers, add a step to attach the `.exe` to the GitHub release.

---

## Acceptance Criteria
- The `make build` command completes without errors.
- A single `.exe` file is generated in the `dist/` directory.
- The generated `.exe` runs the application correctly, with all icons, fonts, and stratagem data loaded and displayed properly.
- The GitHub Actions workflow successfully builds the executable and attaches it to new releases.