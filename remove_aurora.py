import re

with open('app/templates/index.html', 'r') as f:
    content = f.read()

# The aurora background starts with <!-- ── AURORA BACKGROUND LAYER
# and ends right before {% include 'components/toast.html' %}
content = re.sub(
    r'<!-- ── AURORA BACKGROUND LAYER.*?</div>\n*(?=\s*\{%\s*include\s*\'components/toast\.html\'\s*%\})',
    '',
    content,
    flags=re.DOTALL
)

with open('app/templates/index.html', 'w') as f:
    f.write(content)
print("Aurora background removed from index.html")
