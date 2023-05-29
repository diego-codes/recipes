#!/usr/bin/env python
''' Simple script to auto-generate the README.md file for a TIL project, here
    used for a personal cookbook repo. Credit to til-collective for this readme
    generator script.
    Apply as a git hook by running the following command in linux:
        cd .git/hooks/ && ln -s ../../createReadme.py pre-commit && cd -
    To auto-generate the README.md file, you can run
        ./createReadme.py > README.md
    If you are using git, you can install this script as a pre-commit git hook so
    that it is autogenerated on each commit.  Use the following command:
        cd .git/hooks/ && ln -s ../../createReadme.py pre-commit && cd -
    The `.vimrc` file for this project contains a function `CountRecipes` that can
    be invoked with `<leader>c`. This will do a substitution count of the
    current number of recipes and display the result in the command tray.
'''
from __future__ import print_function
import os, posixpath

HEADER = '''# Family recipes
This is a collection of recipes we have learned from our family and friends, or modified
from various cooking sites and apps.
'''

FOOTER = '''## Future recipes
There are a bunch of things we would love to add in the future. If you have a good recipe
for any of the following foods that we could experiment with, please send it our way!
- Pad thai
- Gumbo
- Lasagna
- Curries
- Burrito bowls
- Pasta fresca
- Tacos
- Chili
- Arepas
- Colombian ceviche
- Stir fries
- Sushi
- Wraps
- Nachos (like, real nachos)
- Enchiladas
- Elote

## Credits
- [til-collective/til-collective](https://github.com/til-collective/til-collective)
for autogenerating README

## License
&copy; 2023 Diego and Nic
This repository is licensed under the MIT license. See `LICENSE` for details.
'''


def get_list_of_categories():
    ''' Walk the current directory and get a list of all subdirectories at that
    level. These are the "categories" in which there are recipes.'''
    dirs = [x for x in os.listdir('.') if posixpath.isdir(x) and
            '.git' not in x]
    return dirs


def get_title(recipe_file):
    ''' Read the file until we hit the first line that starts with a #
    indicating a title in markdown. We'll use that as the title for this
    entry. '''
    with open(recipe_file, encoding='UTF-8', errors='ignore') as _file:
        for line in _file:
            line = line.strip()
            if line.startswith('#'):
                return line[1:].lstrip() # text after # and whitespace


def get_recipes(category):
    ''' For a given category, get the list of recipe titles. '''
    recipe_files = [x for x in os.listdir(category)]
    titles = []
    for filename in recipe_files:
        fullname = posixpath.join(category, filename) # here lies the issue
        if (posixpath.isfile(fullname)) and fullname.endswith('.md'):
            title = get_title(fullname)
            titles.append((title, fullname))
    return titles


def get_category_dict(category_names):
    categories = {}
    count = 0
    for category in category_names:
        titles = get_recipes(category)
        categories[category] = titles
        count += len(titles)
    return count, categories


def print_file(category_names, count, categories):
    ''' Now we have all the information, print it out in markdown format. '''
    with open('README.md', 'w', encoding='UTF-8', errors='ignore') as file_:
        file_.write(HEADER)
        file_.write('\n')
        file_.write('We currently have {0} recipes available. For recipes in development, check out [this document](https://docs.google.com/document/d/1xt3ZELFwRy-5zbsjgJlqxuL6pR6px2PWvsmN4Wd8rmI/edit?usp=sharing).'.format(count))
        file_.write('\n')
        file_.write('''
---
### Categories
''')
        # print the list of categories with links
        for category in sorted(category_names):
            file_.write('* [{0}](#{1})\n'.format(category.capitalize().replace('-', ' ') ,
                                                 category))

        # print the section for each category
        file_.write('''
---
''')
        for category in sorted(category_names):
            file_.write('### {0}\n'.format(category.capitalize().replace('-', ' ') ))
            file_.write('\n')
            recipes = categories[category]
            for (title, filename) in sorted(recipes):
                file_.write('- [{0}]({1})\n'.format(title, filename))
            file_.write('\n')

        file_.write(FOOTER)
        print('Generated README successfully with {0} recipes'.format(count))



def create_readme():
    ''' Create a recipe README.md file with a nice index for using it directly
        from github. '''
    category_names = get_list_of_categories()
    count, categories = get_category_dict(category_names)
    print_file(category_names, count, categories)

if __name__ == '__main__':
    create_readme()
    os.system('git add README.md')
