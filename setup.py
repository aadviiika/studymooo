#!/usr/bin/env python3
"""
StudyMoo Setup Script — run once after unzipping.
Usage: python3 setup.py
"""

import os, sys, subprocess, venv

HERE        = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(HERE, 'studymoo_project')
VENV_DIR    = os.path.join(HERE, '.venv')
SEED_FILE   = os.path.join(PROJECT_DIR, '_seed_tmp.py')

def venv_python():
    if sys.platform == 'win32':
        return os.path.join(VENV_DIR, 'Scripts', 'python.exe')
    return os.path.join(VENV_DIR, 'bin', 'python')

def run(args, cwd=None):
    print(f"\n▶  {' '.join(args)}")
    r = subprocess.run(args, cwd=cwd or PROJECT_DIR)
    if r.returncode != 0:
        print("⚠️  Command failed.")
    return r.returncode == 0

def main():
    print("=" * 60)
    print("  🐄  StudyMoo — Setup")
    print("=" * 60)

    # Create venv
    print("\n🔧 Creating virtual environment…")
    if not os.path.exists(VENV_DIR):
        venv.create(VENV_DIR, with_pip=True)
        print("   ✅ .venv/ created")
    else:
        print("   ℹ️  .venv/ already exists")

    py = venv_python()
    req = os.path.join(PROJECT_DIR, 'requirements.txt')

    # Install deps
    print("\n📦 Installing dependencies…")
    run([py, '-m', 'pip', 'install', '--upgrade', 'pip', '-q'])
    run([py, '-m', 'pip', 'install', '-r', req, '-q'])

    # Migrate
    print("\n🗄  Running migrations…")
    run([py, 'manage.py', 'migrate'])

    # Collect static
    print("\n📁 Collecting static files…")
    run([py, 'manage.py', 'collectstatic', '--noinput'])

    # Seed courses
    print("\n🌱 Seeding sample courses…")
    seed = """\
import django, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'studymoo_project.settings'
django.setup()
from resources.models import Course
courses = [
    ('CS101','Introduction to Computer Science'),
    ('MATH201','Calculus II'),
    ('PHYS101','Physics I'),
    ('ENG110','English Composition'),
    ('CHEM101','General Chemistry'),
    ('BIO201','Cell Biology'),
    ('ECON101','Principles of Economics'),
    ('CS301','Data Structures and Algorithms'),
    ('STAT201','Probability and Statistics'),
    ('CS401','Operating Systems'),
]
n = 0
for code, name in courses:
    _, created = Course.objects.get_or_create(code=code, defaults={'name': name})
    if created: n += 1
print('  Created ' + str(n) + ' courses.')
"""
    with open(SEED_FILE, 'w') as f:
        f.write(seed)
    run([py, os.path.basename(SEED_FILE)], cwd=PROJECT_DIR)
    os.remove(SEED_FILE)

    # Superuser
    print("\n👤 Create admin superuser?")
    if input("   [y/N]: ").strip().lower() == 'y':
        run([py, 'manage.py', 'createsuperuser'])

    act = '.venv\\Scripts\\activate' if sys.platform == 'win32' else 'source .venv/bin/activate'
    print("\n" + "=" * 60)
    print("  ✅  Setup complete!")
    print("=" * 60)
    print(f"\n  Start the server:")
    print(f"    {act}")
    print(f"    cd studymoo_project")
    print(f"    python manage.py runserver")
    print(f"\n  Open: http://127.0.0.1:8000")
    print(f"  Admin: http://127.0.0.1:8000/admin/\n")

if __name__ == '__main__':
    main()
