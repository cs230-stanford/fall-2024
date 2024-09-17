import argparse
import csv, re

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--projects-file', required=True, type=str)
    parser.add_argument('--roster-file', required=True, type=str)
    parser.add_argument('--output-file', required=True, type=str)
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

def process_roster(roster_file):
    name_to_sunet = {}
    with open(roster_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            name, sid, email = row[:3]
            # if role == 'Student':
            name_to_sunet[process_name(name)] = process_sunet(email)
    return name_to_sunet

def process_row(row):
    title = row[1]
    names = [process_name(s) for s in row[2:5] if s]
    if len(names) == 0:
        return None
    return title, names

if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()

    name_to_sunet = process_roster(args.roster_file)

    outfile = open(args.output_file, 'w+')
    outwriter = csv.writer(outfile)
    outwriter.writerow(['Title'] + ['Student']*3)

    with open(args.projects_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        for row in rows[1:]:
            processed_row = process_row(row)
            if processed_row is None:
                continue
            title, names = processed_row
            sunets = [name_to_sunet[name] for name in names]
            outwriter.writerow([title] + sunets)
