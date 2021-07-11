#!/bin/bash

set -eo pipefail

git config --global url."https://${GITHUB_TOKEN}@github".insteadOf "https://github"

git config --local user.name "Ben Cunningham"
git config --local user.email "benjamescunningham@gmail.com"
