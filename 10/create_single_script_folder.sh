#!/bin/bash
cd repo
git checkout -f $1
GITOUTPUT=$(git show -s --format=%ci $1)
COMMIT_DATE=$(echo $GITOUTPUT | awk '{ print $1 }')
echo $COMMIT_DATE

mkdir -p ../$COMMIT_DATE
cp script.php ../$COMMIT_DATE/script.php
