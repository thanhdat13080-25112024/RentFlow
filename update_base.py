import re

with open('app/templates/base.html', 'r') as f:
    content = f.read()

# Replace fonts
content = content.replace(
    '<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&display=swap" rel="stylesheet">',
    '<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&family=Roboto+Condensed:wght@500;700&display=swap" rel="stylesheet">'
)
content = content.replace("var(--font-body, 'DM Sans')", "var(--font-body, 'Roboto')")

# Remove aurora background from index.html if present. Oh wait, index.html has the aurora background, which is NOT RentFlow style.
# Let's fix index.html later.

# Map tailwind config to new tokens
tailwind_config = """    tailwind.config = {
      theme: {
        extend: {
          colors: {
            gray: {
              50:  'var(--paper)',
              100: 'var(--surface-2)',
              200: 'var(--line)',
              300: 'var(--line-strong)',
              400: 'var(--ink-3)',
              500: 'var(--ink-2)',
              600: 'var(--ink-2)',
              700: 'var(--ink-1)',
              800: 'var(--ink-1)',
              900: 'var(--ink)',
            },
            violet: {
              50:  'var(--accent-tint)',
              100: 'var(--accent-tint)',
              500: 'var(--accent)',
              600: 'var(--accent)',
              700: 'var(--accent-strong)',
              900: 'var(--accent-strong)',
            },
            blue: {
              50:  'var(--accent-tint)',
              100: 'var(--accent-tint)',
              500: 'var(--accent)',
              600: 'var(--accent)',
              700: 'var(--accent-strong)',
              900: 'var(--accent-strong)',
            },
            sky: {
              500: 'var(--accent)',
            },
            indigo: {
              500: 'var(--accent)',
            },
            cyan: {
              500: 'var(--accent)',
            },
            green: {
              50:  'var(--success-tint)',
              100: 'var(--success-tint)',
              200: 'var(--success-tint)',
              500: 'var(--success)',
              600: 'var(--success)',
              700: 'var(--success)',
            },
            red: {
              50:  'var(--danger-tint)',
              100: 'var(--danger-tint)',
              200: 'var(--danger-tint)',
              500: 'var(--danger)',
              600: 'var(--danger)',
              700: 'var(--danger)',
            },
            amber: {
              50:  'var(--warning-tint)',
              100: 'var(--warning-tint)',
              500: 'var(--warning)',
              600: 'var(--warning)',
            },
          },"""

# Use regex to replace the colors section
content = re.sub(
    r'    tailwind\.config = \{\s*theme: \{\s*extend: \{\s*colors: \{.*?(?=\s*fontFamily:)',
    tailwind_config + '\n',
    content,
    flags=re.DOTALL
)

with open('app/templates/base.html', 'w') as f:
    f.write(content)
print("base.html updated")
