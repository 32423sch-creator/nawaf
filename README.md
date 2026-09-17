name: Streamlit App CI/CD

# تشغيل الـ Workflow عند عمل Push على فرع main أو master
on:
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    # 1. جلب الكود من المستودع
    - name: Checkout code
      uses: actions/checkout@v4

    # 2. إعداد بيئة عمل لغة بايثون
    - name: Set up Python 3.10
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
        cache: 'pip' # تسريع البناء عبر تخزين المكتبات مؤقتاً

    # 3. تثبيت المكتبات البرمجية المطلوبة من ملف requirements.txt
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

    # 4. خطوة فحص اختياري لضمان سلامة تشغيل الكود بدون أخطاء بنيوية
    - name: Lint and Syntax Check
      run: |
        python -m py_compile app.py
