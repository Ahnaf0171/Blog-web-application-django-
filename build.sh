#!/usr/bin/env bash
set -o errexit

# (ঐচ্ছিক) সিস্টেম আপডেট নয়, সরাসরি ডিপেন্ডেন্সি ইন্সটল করুন
pip install -r requirements.txt   # আপনার ফাইলের নাম যদি requirement.txt হয়, সেটা মিলিয়ে নিন

# Django স্টেপস (থাকলে)
python manage.py collectstatic --noinput
python manage.py migrate --noinput
