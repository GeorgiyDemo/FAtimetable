import yaml

outlist = {"telegram_admins" :  [690476,359554]}
with open("out.yml", 'w') as outfile:
    yaml.safe_dump(outlist, outfile, default_flow_style=False, allow_unicode=True)