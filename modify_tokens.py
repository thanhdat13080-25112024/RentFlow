import re

with open('app/static/css/tokens.legacy.css.bak', 'r') as f:
    content = f.read()

# Define the new root block
new_root = """:root {
  /* ---------- RentFlow Design Tokens ---------- */
  --paper:      #F0F0EC;
  --paper-2:    #E8E8E1;
  --surface:    #FBFBF9;
  --surface-2:  #F5F5F1;
  --ink:    #1A1C1D;
  --ink-1:  #373737;
  --ink-2:  #5C5E5C;
  --ink-3:  #8A8C88;
  --on-dark:#F0F0EC;
  --line:        #DCDCD4;
  --line-strong: #C7C7BE;
  --accent:        #466B53;
  --accent-strong: #37553F;
  --accent-tint:   #E3EAE3;
  --accent-on:     #FBFBF9;
  --success:      #3E7A56;  --success-tint: #E4EFE7;
  --warning:      #A9772B;  --warning-tint: #F4EBD8;
  --danger:       #AE453B;  --danger-tint:  #F3E1DE;
  --info:         #3F6B86;  --info-tint:    #E2ECF1;

  /* Brand mapped */
  --color-primary:       var(--accent);
  --color-primary-hover: var(--accent-strong);
  --color-primary-light: var(--accent-tint);
  --color-primary-muted: var(--accent-tint);
  --color-primary-text:  var(--accent-strong);

  /* Status mapped */
  --color-paid:          var(--success);
  --color-paid-bg:       var(--success-tint);
  --color-paid-text:     var(--success);

  --color-unpaid:        var(--danger);
  --color-unpaid-bg:     var(--danger-tint);
  --color-unpaid-text:   var(--danger);

  --color-prepaid:       var(--info);
  --color-prepaid-bg:    var(--info-tint);
  --color-prepaid-text:  var(--info);

  --color-warning:       var(--warning);
  --color-warning-bg:    var(--warning-tint);
  --color-warning-text:  var(--warning);

  /* Surface */
  --color-bg:            var(--paper);
  --color-surface:       var(--surface);
  --color-surface-raised:var(--surface-2);

  /* Border */
  --color-border:        var(--line);
  --color-border-subtle: var(--line);

  /* Text */
  --color-text-primary:  var(--ink);
  --color-text-secondary:var(--ink-1);
  --color-text-tertiary: var(--ink-2);
  --color-text-disabled: var(--ink-3);
  --color-text-inverse:  var(--paper);

  /* Spacing */
  --space-0:  0;
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  12px;
  --space-4:  16px;
  --space-5:  20px;
  --space-6:  24px;
  --space-8:  32px;
  --space-10: 40px;
  --space-12: 48px;

  /* Typography */
  --font-body:    "Roboto", system-ui, -apple-system, sans-serif;
  --font-display: "Roboto SemiCondensed", "Roboto", system-ui, sans-serif;
  --font-cond:    "Roboto Condensed", "Roboto", system-ui, sans-serif;

  --text-xs:   13px;
  --text-sm:   15px;
  --text-base: 17px;
  --text-lg:   19px;
  --text-xl:   22px;
  --text-2xl:  28px;

  --leading-xs:   1.4;
  --leading-sm:   1.5;
  --leading-base: 1.6;
  --leading-lg:   1.4;
  --leading-xl:   1.3;
  --leading-2xl:  1.25;

  /* Radii */
  --radius-sm:   6px;
  --radius-md:   10px;
  --radius-lg:   14px;
  --radius-xl:   20px;
  --radius-2xl:  28px;
  --radius-full: 999px;

  /* Shadows */
  --shadow-xs:  0 1px 2px rgba(26,28,29,.06);
  --shadow-sm:  0 1px 2px rgba(26,28,29,.06);
  --shadow-md:  0 4px 16px -4px rgba(26,28,29,.10);
  --shadow-lg:  0 18px 48px -14px rgba(26,28,29,.16);
  --shadow-xl:  0 18px 48px -14px rgba(26,28,29,.16);
  --shadow-overlay: 0 18px 48px -14px rgba(26,28,29,.16);

  /* Z-index */
  --z-base:     0;
  --z-raised:   1;
  --z-dropdown: 10;
  --z-sticky:   40;
  --z-modal:    50;
  --z-toast:    60;
  --z-top:      9999;

  /* Transitions */
  --ease-out: cubic-bezier(.4,0,.2,1);
  --ease-in:  cubic-bezier(.4,0,.2,1);
  --ease-std: cubic-bezier(.4,0,.2,1);

  --duration-fast:   120ms;
  --duration-normal: 200ms;
  --duration-slow:   360ms;
}"""

# Find the end of the root block in tokens.legacy.css.bak
start_idx = content.find(':root {')
end_idx = content.find('}', start_idx) + 1

if start_idx != -1 and end_idx != -1:
    new_content = new_root + content[end_idx:]
    
    # Also replace any explicit font sizes in utility classes if needed, but keeping them as var() is best
    # Let's replace font-family definitions in the file if any
    new_content = re.sub(r'font-weight:\s*800', 'font-weight: 700', new_content) # Roboto only goes up to 700 or 900, not 800
    new_content = re.sub(r'font-weight:\s*600', 'font-weight: 700', new_content) # Roboto doesn't have 600, use 500 or 700
    
    with open('app/static/css/tokens.css', 'w') as f:
        f.write(new_content)
    print("Successfully replaced :root and updated tokens.css")
else:
    print("Could not find :root block")
