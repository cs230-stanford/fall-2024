#!/usr/bin/env python3

import os
from yaml import load as yaml_load
from yaml import Loader, Dumper
import pandas as pd

def process_report_yaml():
    with open('./project_reports/submission_metadata.yml', 'r') as f:
        report_yaml = yaml_load(f, Loader=Loader)
    # sunet_to_rfn = {}
    rfn_to_names = {}
    rfn_to_ids = {}
    for rfn_long, r_md in report_yaml.items():
        rfn = rfn_long.split('_')[-1]
        names = get_names(r_md)
        ids = get_ids(r_md)
        # for i in ids:
        #     assert i not in sunet_to_rfn
        #     sunet_to_rfn[i] = rfn
        rfn_to_names[rfn] = names
        rfn_to_ids[rfn] = ids
    return rfn_to_names, rfn_to_ids

def get_ids(d):
    ids = set()
    for submitter in d[':submitters']:
        email = submitter[':email']
        suid = email[:email.find('@')]
        assert email.find('@') > 0
        if email.endswith('@stanford.edu'):
            ids.add(suid)
        else:
            print(f'Non-stanford email: {email}')
    return ids

def get_names(d):
    ids = set()
    for submitter in d[':submitters']:
        name = submitter[':name']
        ids.add(name)
    return ids

def get_sunet_to_title():
    sunet_to_title = {}
    sunet_best = set()
    csv = pd.read_csv('project_reports/project_sheet.csv')
    ids = ['id_%d' % (ii + 1) for ii in range(3)]
    csv = csv[ids + ['Title', 'Best']]
    csv = csv.fillna('Missing')
    for index, row in csv.iterrows():
        for idd in ids:
            if row[idd] != 'Missing':
                try:
                    sunet = row[idd].split('@')[0]
                    sunet_to_title[sunet] = row['Title']
                    if row['Best'] == True:
                        sunet_best.add(sunet)
                except Exception as e:
                    print(e)
    return sunet_to_title, sunet_best
            # if row['id_%d' % ii]

def exclude():
    csv = pd.read_csv('project_reports/exclude.csv')
    to_exclude = set()
    for elem in csv['suids']:
        for suid in elem.split(','):
            to_exclude.add(suid)
    return to_exclude

def pull_projects(dirname):
    for folder in os.listdir(dirname):
        if not os.path.isdir("%s/%s" % (dirname, folder)):
            continue
        filename = folder.split('_')[-1] + ".pdf"
        pdf = os.listdir("%s/%s" % (dirname, folder))[0]
        if not pdf.endswith('pdf'):
            continue
        from shutil import copyfile
        src = "%s/%s/%s" % (dirname, folder, pdf)
        dst = "%s/%s" % (dirname, filename)
        copyfile(src, dst)


pull_projects('project_reports/')
rfn_to_names, rfn_to_ids = process_report_yaml()
sunet_to_title, sunet_best = get_sunet_to_title()
to_exclude = exclude()

ROOT = 'http://cs230.stanford.edu'
best_str = "## Outstanding Projects \n\n<ul>\n"
ans_str = "## Submissions\n\n<ul>\n"
exclude_files = []

for rfn, names in rfn_to_names.items():
    sunets = rfn_to_ids[rfn]
    title = ""
    exclude_this = False
    best_this = False
    for sunet in sunets:
        # if sunet == 'sundrani':
        #     breakpoint()
        if sunet in to_exclude:
            exclude_this = True
        if sunet in sunet_best:
            best_this = True
    if exclude_this:
        exclude_files.append(rfn)
        continue
    for sunet in sunets:
        if sunet in sunet_to_title:
            title = sunet_to_title[sunet]
            break
    names = ', '.join(names)
    this_str = f'<li><strong>{title}</strong> by {names}: <a href="{ROOT}/projects_fall_2021/reports/{rfn}.pdf">report</a> </li>\n'
    if best_this:
        best_str += this_str
    else:
        ans_str += this_str
best_str += "\n</ul>"
ans_str += "\n</ul>"

print(exclude_files)

with open('./past_proj_temp.txt', 'w') as temp:
    temp.write(best_str + '\n\n\n' + ans_str)
print("BEST\n%s" % best_str)
print("\n\n\n\n\ALL - BEST\n%s" % ans_str)
exclude_files = ['%s.pdf' % elem for elem in exclude_files]
# Delete These Manually
print('rm ' + ' '.join(exclude_files))
