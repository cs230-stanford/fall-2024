# Requires Python3 with pyyaml
from yaml import load as yaml_load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import argparse
import csv, re

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--projects-file', required=True, type=str)
    parser.add_argument('--roster-file', required=True, type=str)
    parser.add_argument('--reports-metadata', required=True, type=str)
    parser.add_argument('--private-projects-file', required=True, type=str)
    return parser

def process_sunet(x):
    x = x.strip().lower()
    if x == '': return ''
    if '@' in x: x = x[:x.find('@')]
    if re.search('[a-zA-Z]', x) is None:
        return None
    return x

def process_name(x):
    x = x.strip().lower()
    if x == '': return ''
    out = []
    for p in [p for p in x.split(' ')]:
        out.append(p[0].upper() + p[1:])
    return ' '.join(out)

# def process_row(row):
#     title = row[1]; mentor = row[2]
#     names = [process_name(row[i]) for i in (4,6,8,10)]
#     sunets = [process_sunet(row[i]) for i in (5,7,9,11)]
#     names = [x for x in names if x != '']
#     sunets = [x for x in sunets if x != '']
#     if len(names) == 0 or len(sunets) == 0:
#         print(f'  --> Empty name or sunet: {names} // {sunets}')
#         return None
#     if len(names) != len(sunets):
#         print(f'  --> Name and sunet lists length mismatch: {names} // {sunets}')
#         return None
#     for name, sunet in zip(names, sunets):
#         if sunet is None:
#             print(f'  --> Invalid SUNET {sunet} for {name}')
#             return None
#     return title, mentor, names, sunets

def process_row(row):
    title = row[0]
    sunets = [process_sunet(s) for s in row[1:4] if s]
    if len(sunets) == 0:
        return None
    return title, sunets

def process_roster(roster_file):
    sunet_to_name = {}
    with open(roster_file, 'r') as f:
        reader = csv.reader(f)
        # for name, sid, email, role in reader:
            # if role == 'Student':
        for row in reader:
            name, sid, email = row[:3]
            sunet_to_name[process_sunet(email)] = process_name(name)
    return sunet_to_name

def process_teams(projects_file, roster_file):
    sunet_to_title = {}
    sunet_to_team = {}
    sunet_to_name = process_roster(roster_file)
    with open(projects_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        for row in rows[1:]:
            processed_row = process_row(row)
            if processed_row is None:
                continue
            title, sunets = processed_row
            names = [sunet_to_name[sunet] for sunet in sunets]
            skip = False
            for sunet in sunets:
                if sunet in sunet_to_team or sunet in sunet_to_title:
                    print(f'DUPLICATE for {names} // {sunets}')
                    skip = True
            if skip: continue
            for sunet in sunets:    
                sunet_to_title[sunet] = title
                sunet_to_team[sunet] = set(sunets)
    return sunet_to_title, sunet_to_name, sunet_to_team

def process_signups():
    sunet_to_title = {}
    sunet_to_team = {}
    sunet_to_name = {}
    with open('./signups.csv', 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        for row in rows[1:]:
            processed_row = process_row(row)
            if processed_row is None:
                continue
            skip = False
            title, mentor, names, sunets = processed_row
            for name, sunet in zip(names, sunets):
                if sunet in sunet_to_team or sunet in sunet_to_title:
                    print(f'DUPLICATE for {names} // {sunets}')
                    skip = True
            if skip: continue
            for name, sunet in zip(names, sunets):
                sunet_to_title[sunet] = title
                sunet_to_name[sunet] = name
                sunet_to_team[sunet] = set(sunets)
    return sunet_to_title, sunet_to_name, sunet_to_team

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

def process_report_yaml(metadata_file):
    with open(metadata_file, 'r') as f:
        report_yaml = yaml_load(f, Loader=Loader)
    sunet_to_rfn = {}
    for rfn, r_md in report_yaml.items():
        ids = get_ids(r_md)
        for i in ids:
            assert i not in sunet_to_rfn
            sunet_to_rfn[i] = rfn
    return sunet_to_rfn

def process_poster_yaml():
    with open('./posters_orig/submission_metadata.yml', 'r') as f:
        poster_yaml = yaml_load(f, Loader=Loader)
    sunet_to_pfn = {}
    for pfn, p_md in poster_yaml.items():
        ids = get_ids(p_md)
        for i in ids:
            assert i not in sunet_to_pfn
            sunet_to_pfn[i] = pfn
    return sunet_to_pfn

def process_private_projects(private_projects_file):
    with open(private_projects_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
    return set([process_sunet(row[1]) for row in rows[1:]])

if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    sunet_to_title, sunet_to_name, sunet_to_team = process_teams(args.projects_file,
                                                                 args.roster_file)
    sunet_to_rfn = process_report_yaml(args.reports_metadata)
    # sunet_to_pfn = process_poster_yaml()
    private_sunets = process_private_projects(args.private_projects_file)

    ROOT = 'http://cs230.stanford.edu'
    print('<ul>')
    processed = set()
    cnt = 0
    for sunet, title in sunet_to_title.items():
        assert sunet in sunet_to_team and sunet in sunet_to_name
        team = sunet_to_team[sunet]
        skip = False
        for member in team:
            if member in private_sunets or member in processed: skip = True
            processed.add(member)
        if skip: continue
        rfn = sunet_to_rfn.get(sunet, None)
        # pfn = sunet_to_pfn.get(sunet, None)
        pfn = None
        names = ', '.join(sorted([sunet_to_name[t] for t in team]))
        if rfn and pfn:
            print(f'<li><strong>{title}</strong> by {names}: <a href="{ROOT}/projects_spring_2019/reports/{rfn}">report</a> <a href="{ROOT}/projects_winter_2021/posters/{pfn}">poster</a></li>')
        elif rfn:
            print(f'<li><strong>{title}</strong> by {names}: <a href="{ROOT}/projects_winter_2021/reports/{rfn}">report</a></li>')
        elif pfn:
            print(f'<li><strong>{title}</strong> by {names}: <a href="{ROOT}/projects_winter_2021/posters/{pfn}">poster</a></li>')
        cnt += 1
    print('</ul>')
    print(f'\nTotal {cnt} projects populated')


    # Print private files
    print('\n\n  * * * FILES TO DELETE * * *  ')
    print(' '.join([f'reports/{sunet_to_rfn[sunet]}' for sunet in private_sunets if sunet in sunet_to_rfn]))
    print()
    # print(' '.join([f'posters/{sunet_to_pfn[sunet]}' for sunet in private_sunets if sunet in sunet_to_rfn]))
    print()
