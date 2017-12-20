#!/bin/bash -e
# Settings
REPO_PATH=git@github.com:lreis2415/AutoFuzSlpPos.git
HTML_PATH=doc/docstring/_build/html
CHANGESET=$(git rev-parse --verify HEAD)

# Get a clean version of the HTML documentation repo.
rm -rf ${HTML_PATH}
mkdir -p ${HTML_PATH}
git clone -b gh-pages "${REPO_PATH}" --single-branch ${HTML_PATH}

# rm all the files through git to prevent stale files.
cd ${HTML_PATH}
git rm -rf .
git add .
git commit -m "Clean repo."
git push origin gh-pages
cd -

# build the docs
cd doc/docstring
#make clean
make html
cd -

# Create and commit the documentation repo.
cd ${HTML_PATH}
touch .nojekyll
git add .
git commit -m "Automated doc for changeset ${CHANGESET}."
git push origin gh-pages
cd -