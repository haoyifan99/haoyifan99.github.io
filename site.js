/* Progressive enhancement: the complete publication list is readable without JS. */
const filterBar = document.querySelector('[data-publication-filters]');
if (filterBar) {
  filterBar.hidden = false;
  const buttons = [...filterBar.querySelectorAll('button')];
  const papers = [...document.querySelectorAll('[data-topics]')];
  const status = document.querySelector('[data-filter-status]');
  status.hidden = false;
  filterBar.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-filter]');
    if (!button) return;
    const filter = button.dataset.filter;
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    let count = 0;
    papers.forEach(paper => {
      const visible = filter === 'all' || paper.dataset.topics.split(' ').includes(filter);
      paper.hidden = !visible;
      if (visible) count++;
    });
    status.textContent = `Showing ${count} of ${papers.length} works`;
  });
}
