/**
 * Minified by jsDelivr using Terser v5.19.2.
 * Original file: /npm/toastify@2.0.1/dist/build.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
function __extends(t, e) {
  for (var n in e) e.hasOwnProperty(n) && (t[n] = e[n]);
  function i() {
    this.constructor = t;
  }
  t.prototype =
    null === e ? Object.create(e) : ((i.prototype = e.prototype), new i());
}
var BaseLevel = (function () {
    function t() {}
    return (
      (t.prototype.buildNotification = function (t, e, n, i) {
        void 0 === i && (i = null);
        var o = document.createElement("div");
        o.classList.add("toastify"),
          o.classList.add("toastify-" + t.position),
          o.classList.add("toastify-" + e);
        var s = document.createElement("div");
        s.classList.add("toastify-content");
        var r = document.createElement("span");
        r.classList.add("toastify-title"), (r.innerHTML = n);
        var a = document.createElement("span");
        a.classList.add("toastify-content"), (a.innerHTML = i);
        var l = document.createElement("span");
        return (
          l.classList.add("toastify-cancel-icon"),
          (l.innerHTML = "&#x2716;"),
          s.appendChild(r),
          i && s.appendChild(a),
          s.appendChild(l),
          o.appendChild(s),
          o
        );
      }),
      (t.prototype.showNotification = function (t, e) {
        var n = this;
        this.getTarget(e).appendChild(t),
          this.fadeIn(t, e.speed).then(function () {
            n.setUpEventListener(t, e),
              setTimeout(function () {
                n.hideNotification(t, e);
              }, e.delay);
          });
      }),
      (t.prototype.hideNotification = function (t, e) {
        this.fadeOut(t, e.speed).then(function () {
          t.parentNode.removeChild(t);
        });
      }),
      (t.prototype.setUpEventListener = function (t, e) {
        var n = t.lastElementChild;
        n.addEventListener(
          "click",
          function i(o) {
            o.preventDefault(),
              n.removeEventListener("click", i, !1),
              this.hideNotification(t, e);
          }.bind(this)
        );
      }),
      (t.prototype.fadeOut = function (t, e) {
        return new Promise(function (n, i) {
          var o = 1,
            s = setInterval(function () {
              o <= 0.1 && (clearInterval(s), (t.style.display = "none"), n()),
                (t.style.opacity = o.toString()),
                (t.style.filter = "alpha(opacity=" + 100 * o + ")"),
                (o -= 0.1 * o);
            }, e);
        });
      }),
      (t.prototype.fadeIn = function (t, e) {
        return new Promise(function (n, i) {
          var o = 0,
            s = setInterval(function () {
              o > 1 && (clearInterval(s), n()),
                (t.style.opacity = o.toString()),
                (t.style.filter = "alpha(opacity=" + 100 * o + ")"),
                0 !== o ? (o += 0.1 * o) : (o = 0.1);
            }, e);
        });
      }),
      (t.prototype.getTarget = function (t) {
        return "body" !== t.element
          ? document.getElementById(t.element)
          : document.body;
      }),
      t
    );
  })(),
  Success = new ((function (t) {
    function e() {
      t.apply(this, arguments);
    }
    return (
      __extends(e, t),
      (e.prototype.fire = function (t, e, n) {
        void 0 === n && (n = null);
        var i = this.buildNotification(t, "success", e, n);
        this.showNotification(i, t);
      }),
      e
    );
  })(BaseLevel))(),
  Info = new ((function (t) {
    function e() {
      t.apply(this, arguments);
    }
    return (
      __extends(e, t),
      (e.prototype.fire = function (t, e, n) {
        void 0 === n && (n = null);
        var i = this.buildNotification(t, "info", e, n);
        this.showNotification(i, t);
      }),
      e
    );
  })(BaseLevel))(),
  Warning = new ((function (t) {
    function e() {
      t.apply(this, arguments);
    }
    return (
      __extends(e, t),
      (e.prototype.fire = function (t, e, n) {
        void 0 === n && (n = null);
        var i = this.buildNotification(t, "warning", e, n);
        this.showNotification(i, t);
      }),
      e
    );
  })(BaseLevel))(),
  Error = new ((function (t) {
    function e() {
      t.apply(this, arguments);
    }
    return (
      __extends(e, t),
      (e.prototype.fire = function (t, e, n) {
        void 0 === n && (n = null);
        var i = this.buildNotification(t, "error", e, n);
        this.showNotification(i, t);
      }),
      e
    );
  })(BaseLevel))(),
  Default = new ((function (t) {
    function e() {
      t.apply(this, arguments);
    }
    return (
      __extends(e, t),
      (e.prototype.fire = function (t, e, n) {
        void 0 === n && (n = null);
        var i = this.buildNotification(t, "default", e, n);
        this.showNotification(i, t);
      }),
      e
    );
  })(BaseLevel))(),
  Toastify = (function () {
    function t() {
      (this.levels = {
        success: Success,
        info: Info,
        warning: Warning,
        error: Error,
        default: Default,
      }),
        (this.options = {
          position: "bottom-right",
          delay: 5e3,
          speed: 10,
          element: "body",
        });
    }
    return (
      (t.prototype.setOption = function (t, e) {
        if (!this.options.hasOwnProperty(t))
          throw "The option key " + t + " is not a valid option";
        this.options[t] = e;
      }),
      (t.prototype.success = function (t, e) {
        void 0 === e && (e = null),
          this.levels.success.fire(this.options, t, e);
      }),
      (t.prototype.info = function (t, e) {
        void 0 === e && (e = null), this.levels.info.fire(this.options, t, e);
      }),
      (t.prototype.warning = function (t, e) {
        void 0 === e && (e = null),
          this.levels.warning.fire(this.options, t, e);
      }),
      (t.prototype.error = function (t, e) {
        void 0 === e && (e = null), this.levels.error.fire(this.options, t, e);
      }),
      (t.prototype.default = function (t, e) {
        return (
          void 0 === e && (e = null),
          this.levels.default.fire(this.options, t, e)
        );
      }),
      t
    );
  })(),
  index = new Toastify();
export { Toastify };
export default index;
//# sourceMappingURL=/sm/feb64bbd7324425a1e5648341dad7e7a20b33778f2a28492d3fc4146b2155481.map
