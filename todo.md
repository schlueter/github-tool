# For Security Analysis and Mitigation

- For each repository in the org
  ```
  GET /orgs/:org/repos
  ```

  or user
  ```
  GET /users/:username/repos
  ```

  or current user
  ```
  GET /user/repos
  ```

  each with `sort` and `direction` params

  1) check properties:
  - private
  - fork
  - forks_count
  - default branch (ref)
  - open_issues_count
  - is_template
  - has_issues
  - has_projects
  - has_wiki
  - has_pages
  - has_downloads
  - archived
  - disabled
  - visibility (may required additional header, is potentially redundant)
  - pushed_at
  - updated_at
  - created_at
  - template_repository
  - license: key
  1) check branches:
  ```
  GET /repos/:owner/:repo/branches
  ```
  - count
    1) check properties:
    - name
    - protected?
    2) for each protected branch check protection
    ```
    Accept: application/vnd.github.zzzax-preview+json # for sigs
    GET /repos/:owner/:repo/branches/:branch/protection
    ```

    - required_status_checks:
      - strict
      - contexts
    - enforce_admins: enabled?
    - required_pull_request_reviews:
      - dismiss_stale_reviews
      - require_code_owner_reviews
      - required_approving_review_count
      - dismissal_restrictions:
        - users
        - teams
    - restrictions:
      - users
      - teams
      - apps
    - required_linear_history: enabled?
    - allow_force_pushes: enabled?
    - allow_deletions: enabled?
    - required_signatures: enabled?






