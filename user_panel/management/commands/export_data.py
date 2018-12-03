import os
from user_panel.models import *

final_teams = [code.team for code in Code.objects.filter(is_final=True)]
export1_lines = ['Team Name,' +
                 'Member1 FirstName,Member1 LastName,Member1 EnglishName,Member1 Institute' +
                 'Member2 FirstName,Member2 LastName,Member2 EnglishName,Member2 Institute' +
                 'Member3 FirstName,Member3 LastName,Member3 EnglishName,Member3 Institute']
for t in final_teams:
    s = t.name
    for m in t.members.all():
        s += ',{},{},{},{}'.format(m.first_name, m.last_name, m.english_full_name, m.institute)
    export1_lines.append(s)

with open(os.getcwd() + '/export1.csv', 'w+') as f:
    f.write('\n'.join(export1_lines))

export2_lines = ['First Name,Last Name,Email,Phone,Institute,Team Name']
for u in User.objects.all():
    export2_lines.append('{},{},{},{},{},{}'.format(u.first_name, u.last_name, u.email, u.phone, u.institute,
                                                    u.team.name if u.team else '-'))

with open(os.getcwd() + '/export2.csv', 'w+') as f:
    f.writelines('\n'.join(export2_lines))
