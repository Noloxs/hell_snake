# AI Development Guide for Hell Snake Project

This guide provides explicit instructions for AI agents working on the Hell Snake project, focusing on Git and development workflows.

## 1. Setting Up a Clean Development Environment

To ensure a consistent and clean environment for development, follow these steps:

1.  **Revert Local Changes**: Discard any uncommitted local changes and reset your working directory to the last committed state.
    ```bash
    git reset --hard HEAD
    ```
2.  **Switch to Main Branch**: Ensure you are on the `main` branch.
    ```bash
    git checkout main
    ```
3.  **Pull Latest Main**: Pull the latest changes from the remote `main` branch to ensure your local `main` is up-to-date.
    ```bash
    git pull origin main
    ```
4.  **Create New Feature Branch**: Create and switch to a new branch for your development work. Replace `<feature-branch-name>` with a descriptive name for your feature or fix.
    ```bash
    git checkout -b <feature-branch-name>
    ```
4.  **Create Python Virtual Environment**: Set up a dedicated Python virtual environment for the project.
    ```bash
    python -m venv .venv
    ```
5.  **Activate Virtual Environment**: Activate the newly created virtual environment.
    *   **Windows**:
        ```bash
        .venv\Scripts\activate
        ```
    *   **Linux/macOS**:
        ```bash
        . .venv/bin/activate
        ```
6.  **Install Dependencies**: Install all required Python packages listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

## 2. Adding Changes to Git

When you have made changes and are ready to commit them:

1.  **Stage Changes**: Add all modified and new files to the staging area.
    ```bash
    git add .
    ```
2.  **Format Code (Python only)**: If changes involve the Python codebase, run the code formatter to ensure consistent style.
    ```bash
    ruff format .
    ```
3.  **Check Linting (Python only)**: If changes involve the Python codebase, run the linter to identify and fix any code quality issues.
    ```bash
    ruff check .
    ```
4.  **Commit Changes**: Commit the staged changes with a descriptive commit message. Adhere to conventional commit guidelines (e.g., `feat: Add new stratagem`).
    ```bash
    git commit -m "Your descriptive commit message"
    ```
3.  **Inspect Changes (Optional)**: Use the `gh` command-line tool to inspect the status of your changes and tests if needed.
    ```bash
    gh
    ```

## 3. Creating Pull Requests

Once your feature or fix is complete on your branch:

1.  **Ensure Tests Pass (Python only)**: If changes involve the Python codebase, verify that all project tests pass successfully.
    ```bash
    pytest
    ```
2.  **Wait for developer accept**: Query the user with a short summary, whether to proceed. If the user responds affirmatively ('Go', 'Yes', etc.), proceed to the next step. Otherwise, halt the process here.
3.  **Commit and Push**: Ensure all your changes are committed and pushed to your feature branch on the remote repository.
    ```bash
    git push origin <feature-branch-name>
    ```
4.  **Verify GitHub Actions**: Confirm that all automated tests and checks in GitHub Actions pass for your pushed branch.
5.  **Create Pull Request**: Initiate a pull request from your feature branch to the `main` branch.
    *   **Description**: Provide a clear and concise description of your changes, focusing on what aspects require the most review effort.
    *   **Tone**: When describing pull requests, adopt the persona of a "Hell diver" (e.g., "For Super Earth!").
6.  **Assign Reviewers**: Ensure the pull request has an appropriate assignee and reviewer. If unsure, ask for names.

## 4. Reviewing Pull Requests

When reviewing a pull request:

1.  **Ensure a clean environment**: Ensure the environment is clean and ready for work.
2.  **Checkout the Pull Request Branch**: Switch to the pull request branch.
3.  **Understand Changes**: Read the pull request description and review the code changes to understand the purpose and scope of the modifications.
4.  **Check Functionality**: If possible, pull the branch locally and test the changes to ensure they work as intended and do not introduce regressions.
5.  **Provide Feedback**: Offer constructive feedback on code quality, adherence to project conventions, potential bugs, and areas for improvement. Pay attention to wether the description matches the changes.
6.  **Present your decision**: Summarize your findings, and you decision of accepting or requesting futher changes. In the latter case, also describe the changes you deem needed.
7.  **Wait for user confirmation**: Ask the user for confirmation before proceeding. The user may respond with 'Go', 'Yes' or other affirmative responses. The user may also descide to update your understanding, in which case, revise your decision until the user confirms. Otherwise halt the process here.
8.  **Approve or Request Changes**: Based on your review, either approve the pull request or request further changes. Be mindful to include the agreed on description of the review in the review when updating.

## 5. Developer Flow

When implementing changes or features, follow this iterative process:

1.  **Implement Changes**: Make the necessary code modifications to address the task.
2.  **Run Tests**: Execute the project's test suite to verify the changes.
    ```bash
    pytest
    ```
3.  **Iterate on Fixes**: If tests fail, analyze the failures, make further code adjustments, and re-run tests until all tests pass.
4.  **Handle Unresolvable Issues**: If an issue cannot be resolved after reasonable attempts, leave the codebase in the best possible state for the user to debug. This includes:
    *   Ensuring the code is syntactically correct.
    *   Adding comments to highlight the problematic areas and any insights gained during debugging.
    *   Providing a summary of the issue and steps taken to resolve it.
    *   Reverting to a stable state if the changes introduce significant instability.

## 6. Defining a New Feature

When the user requests to define a new feature, follow these steps to define it clearly:

1.  **Understand Requirements**: Analyze the user's description of the feature. If there are ambiguities or missing details, ask clarifying questions.
2.  **Ask Clarifying Questions**: If necessary, ask up to 10 numbered questions to gather more information about the feature. Present these questions in a clear, numbered list to the user.
3.  **Confirm Feature Definition**: Before creating the document, present a summary of the gathered requirements and ask the user for confirmation to proceed with creating the feature description document.
4.  **Create Feature Description Document**: Once the requirements are sufficiently clear and confirmed by the user, create a new Markdown document in the `docs/` folder. The filename should be descriptive of the feature (e.g., `docs/new_stratagem_feature.md`).
5.  **Populate Feature Description**: The document should include the following key points:
    *   **Overview**: A high-level summary of the feature and its purpose.
    *   **Goals**: Specific, measurable, achievable, relevant, and time-bound objectives for the feature.
    *   **User Stories**: Descriptions of the feature from the perspective of different users, outlining their needs and how they will interact with the feature.
    *   **Acceptance Criteria**: A set of conditions that must be met for the feature to be considered complete and working correctly.
6. **Stop**: Offer the user to proceed with breakdown, but do _not_ proceed until the user actually requests this.

## 7. Breaking Down a Feature into Tasks

Once a feature has been defined, follow these steps to break it down into actionable tasks:

1.  **Read Feature Document**: Read and thoroughly understand the feature description document (e.g., `docs/new_stratagem_feature.md`).
2.  **Generate High-Level Tasks**: Based on the feature document, generate a list of high-level tasks required to implement the feature. Present this list to the user for review and acceptance.
3.  **Refine High-Level Tasks**: Interact with the user to refine the high-level task list. Only proceed when the user explicitly accepts the high-level tasks.
4.  **Generate Detailed Subtasks**: For each accepted high-level task, generate a more detailed list of subtasks. These subtasks should be granular enough to be directly actionable. Present this detailed list to the user for review and acceptance.
5.  **Refine Detailed Subtasks**: Interact with the user to refine the detailed subtask list. Only proceed when the user explicitly accepts the detailed subtasks.
6.  **Create Feature TODO Document**: Create a new Markdown document in the `docs/` folder to store the task list. The filename should be related to the feature document (e.g., `docs/new_stratagem_feature_todo.md`).
7.  **Populate Feature TODO Document**: The document should contain the numbered task list with sub-numbering and checkboxes for each task. Here is an example:
    - [ ] 1.0 Parent Task Title
        - [ ] 1.1 [Sub-task description 1.1]
        - [ ] 1.2 [Sub-task description 1.2]
    - [ ] 2.0 Parent Task Title
        - [ ] 2.1 [Sub-task description 2.1]
    - [ ] 3.0 Parent Task Title (may not require sub-tasks if purely structural or configuration)
8. **Stop**: Do _not_ proceed with implementation until the user actually requests this.