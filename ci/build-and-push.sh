#!/bin/bash

set -eo pipefail

if [ -z "${GIT_CURRENT_BRANCH}" ]; then
    GIT_CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
fi

echo "Current branch: ${GIT_CURRENT_BRANCH}"

if [ "${GIT_CURRENT_BRANCH}" = "main" ]; then

    git checkout -t origin/main

    make install
    make build

    git add README.md
    git status

    GIT_FILES_ARE_STAGED=$(git diff --cached)

    if [ -n "${GIT_FILES_ARE_STAGED}" ]; then
        git commit -m "Autobuild dashboard"
        git push origin main
    else
        echo "Nothing to commit."
    fi

else

    echo "Refusing to build dashboard since current branch is not main."

fi

git checkout ${GIT_CURRENT_BRANCH} --
