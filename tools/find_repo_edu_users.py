#!/usr/bin/env python

import getpass
from github import Github


def is_edu_user(user):
    is_univ = False
    is_edu_email = False
    if not user.company is None:
        company = user.company.lower()
        if "university" in company or "academy" in company or "science" in company or "technology" in company or "tech" in company or "college" in company or "institute" in company:
            is_univ = True
    if not user.email is None:
        email = user.email.lower()
        if "edu" in email or "ac.cn" in email or "ac.uk" in email or "ac.ir" in email or "ac.il" in email or "ac.jp" in email or "ac.nz" in email or "ac.kr" in email:
            is_edu_email = True
    if is_univ or is_edu_email:
        return True
    else:
        return False


def print_user(user):
    print("User URL:", user.html_url)
    print("User Email:", user.email)
    print("User Company:", user.company)
    print("User Location:", user.location)
    print("User Blog:", user.blog)
    print("User Bio:", user.bio)


login = input("Enter your Github login: ")
p = getpass.getpass(prompt="Enter your password: ")
g = Github(login, p)
print("Authenticated successfully, now let's pull some conflict-of-interest information...")
repo = g.get_repo("commaai/openpilot")


open_pulls = repo.get_pulls(state='open', sort='created', base='devel')
for pr in open_pulls:
    user = g.get_user(pr.user.login)
    if is_edu_user(user):
        print("PR:", pr)
        print_user(user)
        print()


closed_pulls = repo.get_pulls(state='closed', sort='created', base='devel')
for pr in closed_pulls:
    user = g.get_user(pr.user.login)
    if is_edu_user(user):
        print("PR:", pr)
        print_user(user)
        print()


open_issues = repo.get_issues(state='open')
for issue in open_issues:
    user = g.get_user(issue.user.login)
    if is_edu_user(user):
        print("Issue:", issue)
        print_user(user)
        print()


closed_issues = repo.get_issues(state='closed')
for issue in closed_issues:
    user = g.get_user(issue.user.login)
    if is_edu_user(user):
        print("Issue:", issue)
        print_user(user)
        print()
