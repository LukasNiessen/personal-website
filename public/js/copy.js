(() => {
  function initCopyButtons() {
    document.querySelectorAll('pre > code').forEach((code) => {
      const pre = code.parentElement;
      if (pre.parentElement.classList.contains('code-block')) return;

      // Keep the toolbar outside the scrolling pre so it stays in its corner.
      const wrapper = document.createElement('div');
      wrapper.className = 'code-block';
      // Preserve contextual prose spacing, such as the reset after a heading.
      const spacing = getComputedStyle(pre);
      wrapper.style.marginTop = spacing.marginTop;
      wrapper.style.marginBottom = spacing.marginBottom;
      pre.style.marginTop = '0';
      pre.style.marginBottom = '0';
      pre.before(wrapper);
      wrapper.appendChild(pre);

      const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
      use.setAttribute('href', '/copy.svg#empty');
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.classList.add('copy-svg');
      svg.setAttribute('aria-hidden', 'true');
      svg.appendChild(use);

      const label = document.createElement('span');
      label.textContent = 'Copy';
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'copy-btn';
      button.setAttribute('aria-label', 'Copy code to clipboard');
      button.append(svg, label);

      const status = document.createElement('span');
      status.className = 'sr-only';
      status.setAttribute('role', 'status');
      status.setAttribute('aria-live', 'polite');
      status.setAttribute('aria-atomic', 'true');

      const toolbar = document.createElement('div');
      toolbar.className = 'copy-cnt';
      toolbar.append(button, status);
      wrapper.appendChild(toolbar);

      let resetTimer;
      let copying = false;
      button.addEventListener('click', async () => {
        if (copying) return;
        clearTimeout(resetTimer);
        copying = true;
        button.setAttribute('aria-disabled', 'true');
        status.textContent = '';

        try {
          // textContent preserves indentation and line breaks without including
          // the toolbar or depending on how the browser lays out the code.
          await navigator.clipboard.writeText(code.textContent || '');
          label.textContent = 'Copied!';
          use.setAttribute('href', '/copy.svg#filled');
          status.textContent = 'Code copied to clipboard.';
        } catch {
          label.textContent = 'Copy failed';
          use.setAttribute('href', '/copy.svg#empty');
          status.textContent = 'Copy failed. Select and copy the code manually, or try again.';
        } finally {
          copying = false;
          button.removeAttribute('aria-disabled');
          resetTimer = setTimeout(() => {
            label.textContent = 'Copy';
            use.setAttribute('href', '/copy.svg#empty');
          }, 2500);
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCopyButtons, { once: true });
  } else {
    initCopyButtons();
  }
  document.addEventListener('astro:page-load', initCopyButtons);
})();
