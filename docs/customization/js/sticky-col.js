document$.subscribe(function () {
    document.querySelectorAll('.md-typeset__scrollwrap').forEach(function (wrap) {
        var cells = Array.from(wrap.querySelectorAll('td:first-child, th:first-child'));
        if (cells.length === 0) return;

        var pending = false;

        function update() {
            var x = wrap.scrollLeft + 'px';
            cells.forEach(function (cell) {
                cell.style.transform = 'translateX(' + x + ')';
            });
            pending = false;
        }

        wrap.addEventListener('scroll', function () {
            if (!pending) {
                pending = true;
                requestAnimationFrame(update);
            }
        }, { passive: true });

        update();
    });
});
