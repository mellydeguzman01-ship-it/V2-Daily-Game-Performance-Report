
    /* Night mode is applied before first paint so a returning visitor who
       chose it never sees a flash of the light theme. */
    (function () {
      var KEY = 'dashboard-theme';
      var read = function () {
        try { return localStorage.getItem(KEY) === 'night'; } catch (e) { return false; }
      };
      var apply = function (on) {
        document.documentElement.classList.toggle('night', on);
        var b = document.getElementById('nightModeButton');
        if (b) b.setAttribute('aria-pressed', on ? 'true' : 'false');
      };
      apply(read());
      document.addEventListener('DOMContentLoaded', function () {
        var b = document.getElementById('nightModeButton');
        if (!b) return;
        // the button does not exist yet when the class is applied above, so
        // its pressed state has to be synced once it is in the DOM
        apply(document.documentElement.classList.contains('night'));
        b.addEventListener('click', function () {
          var on = !document.documentElement.classList.contains('night');
          apply(on);
          try { localStorage.setItem(KEY, on ? 'night' : 'light'); } catch (e) {}
        });
      });
    })();
  