import datetime, json, os, sys, time
from git import Repo, Git


# Set your GitHub username
username = 'nerdymark'
repo_name = 'contribution-marquee'
git_ssh_identity_file = 'marquee'
git_ssh_cmd = 'ssh -i %s' % git_ssh_identity_file

# Load the json file

data = json.loads(open('marquee-data.json').read())

# Delete the cached repo if it exists
if os.path.exists(repo_name):
    os.system('rm -rf {}'.format(repo_name))
    print('Deleted {}'.format(repo_name))

repo = Repo.clone_from('git@github.com:nerdymark/contribution-marquee.git', 'contribution-marquee', env=dict(GIT_SSH_COMMAND=git_ssh_cmd))
# origin = repo.remote(name='origin')

for letter in data:
    for date in next(iter(letter.values())):
        today_date = datetime.datetime.now().date().isoformat()
        if date['date'] == today_date and date['index'] is not None:
            print('Today is {}!'.format(date['date']))

            # Get index of today
            today_index = date['index']
            if type(today_index) == int:
                print('Today we need to contribute {} more times.'.format(today_index + 1))

                
                # Add a string to test.txt
                file_path = 'test.txt'.format(repo_name)
                with open(file_path, 'a') as f:
                    f.write('test')

                repo.index.add([file_path])
                repo.index.commit('Contribution Marquee: {}'.format(today_date))
                repo.remote().push()
                
                # Decrement index by 1, save to json
                if date['index'] == 0:
                    date['index'] = None
                else:
                    date['index'] = today_index - 1
                
                # Save the file
                with open('marquee-data.json', 'w') as outfile:
                    outfile.write(json.dumps(data, indent=4))
        elif date['date'] == today_date and date['index'] is None:
            print('Today is {}!'.format(date['date']))
            print('We have already contributed today.')
