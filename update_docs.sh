#!/usr/bin/env bash
# http://www.willmcginnis.com/2016/02/29/automating-documentation-workflow-with-sphinx-and-github-pages/
# build the docs
cd doc/docstring
make clean
make html
cd ../..
# commit and push
git add -A
git commit -m "building and pushing docs"
git push -u origin master
# switch branches and pull the data we want
git checkout gh-pages
touch .nojekyll
# delete older files
rm -rf ./_modules
rm -rf ./_sources
rm -rf ./_static
rm -f *.html
rm -f *.inv
rm -f *.js
# move new files to current branch
mv ./doc/docstring/_build/html/* ./
git status
git add .
# delete
rm -rf ./doc
rm -rf ./data
rm -rf ./autofuzslppos
rm -rf ./test
# add, commit, and push
git add -A
git commit -m "publishing updated docs..."
git push -u origin gh-pages
# switch back
git checkout master