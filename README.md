# tuxpkg - release automation tool for Python projects

## gitlab CI pipeline

How to use:

```yaml
include:
  - https://gitlab.com/Linaro/tuxpkg/raw/main/gitlab-ci-pipeline.yml
variables:
  # ... override variables here (see below)
```

Variables that can be overriden locally:

- `TUXPKG`: how to call tuxpkg. Default: `tuxpkg`.

The following protected variables need to be set in the CI/CD configuration:

- `TUXPKG_RELEASE_KEY`: a variable of type "file", containing an ascii-armored
  export of gnupg private key to sign the package repositories.  Because the
  private key will be uploaded into GitLab CI, you want to create a new GPG key
  for your project only. DO NOT upload your own private key! :-)
  The command to export the key is `gpg --export-private-keys --armor KEYID`.
- `TUXPKG_RELEASE_KEYID`: the public gnupg key ID used to sign the package
  repositories. The is the full GPG key id, e.g.
  `1EC68783C596C4AD1C2E45896D082F7024A0AEAF`.
- `FLIT_PASSWORD`: password to authenticate to PyPI with. Generate a
  project-specific token. `FLIT_USERNAME` will be automatically set to
  `__token__`.
