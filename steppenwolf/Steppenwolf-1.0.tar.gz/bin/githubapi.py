#!/usr/bin/env python3

import os, re, sys

from github import Github

from Spanners.Squirrel import Squirrel

squirrel = Squirrel()

hostname='github.com'
tokenname='rescript'
token=squirrel.get('%s:%s'%(hostname, tokenname))

gh = Github(token)

for repo in gh.get_user().get_repos():
	print(repo.name)


	
