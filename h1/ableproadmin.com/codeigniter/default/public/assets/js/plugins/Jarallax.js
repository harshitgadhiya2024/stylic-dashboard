/*!
 * Name    : Just Another Parallax [Jarallax]
 * Version : 1.10.7
 * Author  : nK <https://nkdev.info>
 * GitHub  : https://github.com/nk-o/jarallax
 */ !(function (o) {
  var n = {};
  function i(e) {
    if (n[e]) return n[e].exports;
    var t = (n[e] = { i: e, l: !1, exports: {} });
    return o[e].call(t.exports, t, t.exports, i), (t.l = !0), t.exports;
  }
  (i.m = o),
    (i.c = n),
    (i.d = function (e, t, o) {
      i.o(e, t) || Object.defineProperty(e, t, { enumerable: !0, get: o });
    }),
    (i.r = function (e) {
      'undefined' != typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, { value: 'Module' }),
        Object.defineProperty(e, '__esModule', { value: !0 });
    }),
    (i.t = function (t, e) {
      if ((1 & e && (t = i(t)), 8 & e)) return t;
      if (4 & e && 'object' == typeof t && t && t.__esModule) return t;
      var o = Object.create(null);
      if ((i.r(o), Object.defineProperty(o, 'default', { enumerable: !0, value: t }), 2 & e && 'string' != typeof t))
        for (var n in t)
          i.d(
            o,
            n,
            function (e) {
              return t[e];
            }.bind(null, n)
          );
      return o;
    }),
    (i.n = function (e) {
      var t =
        e && e.__esModule
          ? function () {
              return e.default;
            }
          : function () {
              return e;
            };
      return i.d(t, 'a', t), t;
    }),
    (i.o = function (e, t) {
      return Object.prototype.hasOwnProperty.call(e, t);
    }),
    (i.p = ''),
    i((i.s = 11));
})([
  ,
  ,
  function (e, t, o) {
    'use strict';
    e.exports = function (e) {
      'complete' === document.readyState || 'interactive' === document.readyState
        ? e.call()
        : document.attachEvent
          ? document.attachEvent('onreadystatechange', function () {
              'interactive' === document.readyState && e.call();
            })
          : document.addEventListener && document.addEventListener('DOMContentLoaded', e);
    };
  },
  ,
  function (o, e, t) {
    'use strict';
    (function (e) {
      var t;
      (t = 'undefined' != typeof window ? window : void 0 !== e ? e : 'undefined' != typeof self ? self : {}), (o.exports = t);
    }).call(this, t(5));
  },
  function (e, t, o) {
    'use strict';
    var n,
      i =
        'function' == typeof Symbol && 'symbol' == typeof Symbol.iterator
          ? function (e) {
              return typeof e;
            }
          : function (e) {
              return e && 'function' == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? 'symbol' : typeof e;
            };
    n = (function () {
      return this;
    })();
    try {
      n = n || Function('return this')() || (0, eval)('this');
    } catch (e) {
      'object' === ('undefined' == typeof window ? 'undefined' : i(window)) && (n = window);
    }
    e.exports = n;
  },
  ,
  ,
  ,
  ,
  ,
  function (e, t, o) {
    e.exports = o(12);
  },
  function (e, t, o) {
    'use strict';
    var n =
        'function' == typeof Symbol && 'symbol' == typeof Symbol.iterator
          ? function (e) {
              return typeof e;
            }
          : function (e) {
              return e && 'function' == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? 'symbol' : typeof e;
            },
      i = l(o(2)),
      a = o(4),
      r = l(o(13));
    function l(e) {
      return e && e.__esModule ? e : { default: e };
    }
    var s = a.window.jarallax;
    if (
      ((a.window.jarallax = r.default),
      (a.window.jarallax.noConflict = function () {
        return (a.window.jarallax = s), this;
      }),
      void 0 !== a.jQuery)
    ) {
      var c = function () {
        var e = arguments || [];
        Array.prototype.unshift.call(e, this);
        var t = r.default.apply(a.window, e);
        return 'object' !== (void 0 === t ? 'undefined' : n(t)) ? t : this;
      };
      c.constructor = r.default.constructor;
      var u = a.jQuery.fn.jarallax;
      (a.jQuery.fn.jarallax = c),
        (a.jQuery.fn.jarallax.noConflict = function () {
          return (a.jQuery.fn.jarallax = u), this;
        });
    }
    (0, i.default)(function () {
      (0, r.default)(document.querySelectorAll('[data-jarallax]'));
    });
  },
  function (e, j, S) {
    'use strict';
    (function (e) {
      Object.defineProperty(j, '__esModule', { value: !0 });
      var d = function (e, t) {
          if (Array.isArray(e)) return e;
          if (Symbol.iterator in Object(e))
            return (function (e, t) {
              var o = [],
                n = !0,
                i = !1,
                a = void 0;
              try {
                for (var r, l = e[Symbol.iterator](); !(n = (r = l.next()).done) && (o.push(r.value), !t || o.length !== t); n = !0);
              } catch (e) {
                (i = !0), (a = e);
              } finally {
                try {
                  !n && l.return && l.return();
                } finally {
                  if (i) throw a;
                }
              }
              return o;
            })(e, t);
          throw new TypeError('Invalid attempt to destructure non-iterable instance');
        },
        t = (function () {
          function n(e, t) {
            for (var o = 0; o < t.length; o++) {
              var n = t[o];
              (n.enumerable = n.enumerable || !1),
                (n.configurable = !0),
                'value' in n && (n.writable = !0),
                Object.defineProperty(e, n.key, n);
            }
          }
          return function (e, t, o) {
            return t && n(e.prototype, t), o && n(e, o), e;
          };
        })(),
        p =
          'function' == typeof Symbol && 'symbol' == typeof Symbol.iterator
            ? function (e) {
                return typeof e;
              }
            : function (e) {
                return e && 'function' == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? 'symbol' : typeof e;
              },
        o = a(S(2)),
        n = a(S(14)),
        i = S(4);
      function a(e) {
        return e && e.__esModule ? e : { default: e };
      }
      var s =
          -1 < navigator.userAgent.indexOf('MSIE ') ||
          -1 < navigator.userAgent.indexOf('Trident/index.html') ||
          -1 < navigator.userAgent.indexOf('Edge/index-2.html'),
        r = (function () {
          for (var e = 'transform WebkitTransform MozTransform'.split(' '), t = document.createElement('div'), o = 0; o < e.length; o++)
            if (t && void 0 !== t.style[e[o]]) return e[o];
          return !1;
        })(),
        b = void 0,
        v = void 0,
        l = void 0,
        c = !1,
        u = !1;
      function m(e) {
        (b = i.window.innerWidth || document.documentElement.clientWidth),
          (v = i.window.innerHeight || document.documentElement.clientHeight),
          'object' !== (void 0 === e ? 'undefined' : p(e)) || ('load' !== e.type && 'dom-loaded' !== e.type) || (c = !0);
      }
      m(),
        i.window.addEventListener('resize', m),
        i.window.addEventListener('orientationchange', m),
        i.window.addEventListener('load', m),
        (0, o.default)(function () {
          m({ type: 'dom-loaded' });
        });
      var f = [],
        y = !1;
      function g() {
        if (f.length) {
          l =
            void 0 !== i.window.pageYOffset
              ? i.window.pageYOffset
              : (document.documentElement || document.body.parentNode || document.body).scrollTop;
          var t = c || !y || y.width !== b || y.height !== v,
            o = u || t || !y || y.y !== l;
          (u = c = !1),
            (t || o) &&
              (f.forEach(function (e) {
                t && e.onResize(), o && e.onScroll();
              }),
              (y = { width: b, height: v, y: l })),
            (0, n.default)(g);
        }
      }
      var h =
          !!e.ResizeObserver &&
          new e.ResizeObserver(function (e) {
            e &&
              e.length &&
              (0, n.default)(function () {
                e.forEach(function (e) {
                  e.target && e.target.jarallax && (c || e.target.jarallax.onResize(), (u = !0));
                });
              });
          }),
        x = 0,
        w = (function () {
          function u(e, t) {
            !(function (e, t) {
              if (!(e instanceof t)) throw new TypeError('Cannot call a class as a function');
            })(this, u);
            var o = this;
            (o.instanceID = x++),
              (o.$item = e),
              (o.defaults = {
                type: 'scroll',
                speed: 0.5,
                imgSrc: null,
                imgElement: '.jarallax-img',
                imgSize: 'cover',
                imgPosition: '50% 50%',
                imgRepeat: 'no-repeat',
                keepImg: !1,
                elementInViewport: null,
                zIndex: -100,
                disableParallax: !1,
                disableVideo: !1,
                automaticResize: !0,
                videoSrc: null,
                videoStartTime: 0,
                videoEndTime: 0,
                videoVolume: 0,
                videoLoop: !0,
                videoPlayOnlyVisible: !0,
                onScroll: null,
                onInit: null,
                onDestroy: null,
                onCoverImage: null
              });
            var n = o.$item.getAttribute('data-jarallax'),
              i = JSON.parse(n || '{}');
            n &&
              console.warn(
                'Detected usage of deprecated data-jarallax JSON options, you should use pure data-attribute options. See info here - https://github.com/nk-o/jarallax/issues/53'
              );
            var a = o.$item.dataset || {},
              r = {};
            if (
              (Object.keys(a).forEach(function (e) {
                var t = e.substr(0, 1).toLowerCase() + e.substr(1);
                t && void 0 !== o.defaults[t] && (r[t] = a[e]);
              }),
              (o.options = o.extend({}, o.defaults, i, r, t)),
              (o.pureOptions = o.extend({}, o.options)),
              Object.keys(o.options).forEach(function (e) {
                'true' === o.options[e] ? (o.options[e] = !0) : 'false' === o.options[e] && (o.options[e] = !1);
              }),
              (o.options.speed = Math.min(2, Math.max(-1, parseFloat(o.options.speed)))),
              (o.options.noAndroid || o.options.noIos) &&
                (console.warn(
                  'Detected usage of deprecated noAndroid or noIos options, you should use disableParallax option. See info here - https://github.com/nk-o/jarallax/#disable-on-mobile-devices'
                ),
                o.options.disableParallax ||
                  (o.options.noIos && o.options.noAndroid
                    ? (o.options.disableParallax = /iPad|iPhone|iPod|Android/)
                    : o.options.noIos
                      ? (o.options.disableParallax = /iPad|iPhone|iPod/)
                      : o.options.noAndroid && (o.options.disableParallax = /Android/))),
              'string' == typeof o.options.disableParallax && (o.options.disableParallax = new RegExp(o.options.disableParallax)),
              o.options.disableParallax instanceof RegExp)
            ) {
              var l = o.options.disableParallax;
              o.options.disableParallax = function () {
                return l.test(navigator.userAgent);
              };
            }
            if (
              ('function' != typeof o.options.disableParallax &&
                (o.options.disableParallax = function () {
                  return !1;
                }),
              'string' == typeof o.options.disableVideo && (o.options.disableVideo = new RegExp(o.options.disableVideo)),
              o.options.disableVideo instanceof RegExp)
            ) {
              var s = o.options.disableVideo;
              o.options.disableVideo = function () {
                return s.test(navigator.userAgent);
              };
            }
            'function' != typeof o.options.disableVideo &&
              (o.options.disableVideo = function () {
                return !1;
              });
            var c = o.options.elementInViewport;
            c && 'object' === (void 0 === c ? 'undefined' : p(c)) && void 0 !== c.length && (c = d(c, 1)[0]);
            c instanceof Element || (c = null),
              (o.options.elementInViewport = c),
              (o.image = {
                src: o.options.imgSrc || null,
                $container: null,
                useImgTag: !1,
                position: /iPad|iPhone|iPod|Android/.test(navigator.userAgent) ? 'absolute' : 'fixed'
              }),
              o.initImg() && o.canInitParallax() && o.init();
          }
          return (
            t(u, [
              {
                key: 'css',
                value: function (t, o) {
                  return 'string' == typeof o
                    ? i.window.getComputedStyle(t).getPropertyValue(o)
                    : (o.transform && r && (o[r] = o.transform),
                      Object.keys(o).forEach(function (e) {
                        t.style[e] = o[e];
                      }),
                      t);
                }
              },
              {
                key: 'extend',
                value: function (o) {
                  var n = arguments;
                  return (
                    (o = o || {}),
                    Object.keys(arguments).forEach(function (t) {
                      n[t] &&
                        Object.keys(n[t]).forEach(function (e) {
                          o[e] = n[t][e];
                        });
                    }),
                    o
                  );
                }
              },
              {
                key: 'getWindowData',
                value: function () {
                  return { width: b, height: v, y: l };
                }
              },
              {
                key: 'initImg',
                value: function () {
                  var e = this,
                    t = e.options.imgElement;
                  return (
                    t && 'string' == typeof t && (t = e.$item.querySelector(t)),
                    t instanceof Element || (t = null),
                    t &&
                      (e.options.keepImg ? (e.image.$item = t.cloneNode(!0)) : ((e.image.$item = t), (e.image.$itemParent = t.parentNode)),
                      (e.image.useImgTag = !0)),
                    !!e.image.$item ||
                      (null === e.image.src &&
                        (e.image.src = e
                          .css(e.$item, 'background-image')
                          .replace(/^url\(['"]?/g, '')
                          .replace(/['"]?\)$/g, '')),
                      !(!e.image.src || 'none' === e.image.src))
                  );
                }
              },
              {
                key: 'canInitParallax',
                value: function () {
                  return r && !this.options.disableParallax();
                }
              },
              {
                key: 'init',
                value: function () {
                  var e = this,
                    t = { position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', overflow: 'hidden', pointerEvents: 'none' },
                    o = {};
                  if (!e.options.keepImg) {
                    var n = e.$item.getAttribute('style');
                    if ((n && e.$item.setAttribute('data-jarallax-original-styles', n), e.image.useImgTag)) {
                      var i = e.image.$item.getAttribute('style');
                      i && e.image.$item.setAttribute('data-jarallax-original-styles', i);
                    }
                  }
                  if (
                    ('static' === e.css(e.$item, 'position') && e.css(e.$item, { position: 'relative' }),
                    'auto' === e.css(e.$item, 'z-index') && e.css(e.$item, { zIndex: 0 }),
                    (e.image.$container = document.createElement('div')),
                    e.css(e.image.$container, t),
                    e.css(e.image.$container, { 'z-index': e.options.zIndex }),
                    s && e.css(e.image.$container, { opacity: 0.9999 }),
                    e.image.$container.setAttribute('id', 'jarallax-container-' + e.instanceID),
                    e.$item.appendChild(e.image.$container),
                    e.image.useImgTag
                      ? (o = e.extend(
                          {
                            'object-fit': e.options.imgSize,
                            'object-position': e.options.imgPosition,
                            'font-family': 'object-fit: ' + e.options.imgSize + '; object-position: ' + e.options.imgPosition + ';',
                            'max-width': 'none'
                          },
                          t,
                          o
                        ))
                      : ((e.image.$item = document.createElement('div')),
                        e.image.src &&
                          (o = e.extend(
                            {
                              'background-position': e.options.imgPosition,
                              'background-size': e.options.imgSize,
                              'background-repeat': e.options.imgRepeat,
                              'background-image': 'url("' + e.image.src + '")'
                            },
                            t,
                            o
                          ))),
                    ('opacity' !== e.options.type &&
                      'scale' !== e.options.type &&
                      'scale-opacity' !== e.options.type &&
                      1 !== e.options.speed) ||
                      (e.image.position = 'absolute'),
                    'fixed' === e.image.position)
                  )
                    for (var a = 0, r = e.$item; null !== r && r !== document && 0 === a; ) {
                      var l = e.css(r, '-webkit-transform') || e.css(r, '-moz-transform') || e.css(r, 'transform');
                      l && 'none' !== l && ((a = 1), (e.image.position = 'absolute')), (r = r.parentNode);
                    }
                  (o.position = e.image.position),
                    e.css(e.image.$item, o),
                    e.image.$container.appendChild(e.image.$item),
                    e.onResize(),
                    e.onScroll(!0),
                    e.options.automaticResize && h && h.observe(e.$item),
                    e.options.onInit && e.options.onInit.call(e),
                    'none' !== e.css(e.$item, 'background-image') && e.css(e.$item, { 'background-image': 'none' }),
                    e.addToParallaxList();
                }
              },
              {
                key: 'addToParallaxList',
                value: function () {
                  f.push(this), 1 === f.length && g();
                }
              },
              {
                key: 'removeFromParallaxList',
                value: function () {
                  var o = this;
                  f.forEach(function (e, t) {
                    e.instanceID === o.instanceID && f.splice(t, 1);
                  });
                }
              },
              {
                key: 'destroy',
                value: function () {
                  var e = this;
                  e.removeFromParallaxList();
                  var t = e.$item.getAttribute('data-jarallax-original-styles');
                  if (
                    (e.$item.removeAttribute('data-jarallax-original-styles'),
                    t ? e.$item.setAttribute('style', t) : e.$item.removeAttribute('style'),
                    e.image.useImgTag)
                  ) {
                    var o = e.image.$item.getAttribute('data-jarallax-original-styles');
                    e.image.$item.removeAttribute('data-jarallax-original-styles'),
                      o ? e.image.$item.setAttribute('style', t) : e.image.$item.removeAttribute('style'),
                      e.image.$itemParent && e.image.$itemParent.appendChild(e.image.$item);
                  }
                  e.$clipStyles && e.$clipStyles.parentNode.removeChild(e.$clipStyles),
                    e.image.$container && e.image.$container.parentNode.removeChild(e.image.$container),
                    e.options.onDestroy && e.options.onDestroy.call(e),
                    delete e.$item.jarallax;
                }
              },
              {
                key: 'clipContainer',
                value: function () {
                  if ('fixed' === this.image.position) {
                    var e = this,
                      t = e.image.$container.getBoundingClientRect(),
                      o = t.width,
                      n = t.height;
                    if (!e.$clipStyles)
                      (e.$clipStyles = document.createElement('style')),
                        e.$clipStyles.setAttribute('type', 'text/css'),
                        e.$clipStyles.setAttribute('id', 'jarallax-clip-' + e.instanceID),
                        (document.head || document.getElementsByTagName('head')[0]).appendChild(e.$clipStyles);
                    var i =
                      '#jarallax-container-' +
                      e.instanceID +
                      ' {\n           clip: rect(0 ' +
                      o +
                      'px ' +
                      n +
                      'px 0);\n           clip: rect(0, ' +
                      o +
                      'px, ' +
                      n +
                      'px, 0);\n        }';
                    e.$clipStyles.styleSheet ? (e.$clipStyles.styleSheet.cssText = i) : (e.$clipStyles.innerHTML = i);
                  }
                }
              },
              {
                key: 'coverImage',
                value: function () {
                  var e = this,
                    t = e.image.$container.getBoundingClientRect(),
                    o = t.height,
                    n = e.options.speed,
                    i = 'scroll' === e.options.type || 'scroll-opacity' === e.options.type,
                    a = 0,
                    r = o,
                    l = 0;
                  return (
                    i &&
                      (n < 0 ? ((a = n * Math.max(o, v)), v < o && (a -= n * (o - v))) : (a = n * (o + v)),
                      1 < n ? (r = Math.abs(a - v)) : n < 0 ? (r = a / n + Math.abs(a)) : (r += (v - o) * (1 - n)),
                      (a /= 2)),
                    (e.parallaxScrollDistance = a),
                    (l = i ? (v - r) / 2 : (o - r) / 2),
                    e.css(e.image.$item, {
                      height: r + 'px',
                      marginTop: l + 'px',
                      left: 'fixed' === e.image.position ? t.left + 'px' : '0',
                      width: t.width + 'px'
                    }),
                    e.options.onCoverImage && e.options.onCoverImage.call(e),
                    { image: { height: r, marginTop: l }, container: t }
                  );
                }
              },
              {
                key: 'isVisible',
                value: function () {
                  return this.isElementInViewport || !1;
                }
              },
              {
                key: 'onScroll',
                value: function (e) {
                  var t = this,
                    o = t.$item.getBoundingClientRect(),
                    n = o.top,
                    i = o.height,
                    a = {},
                    r = o;
                  if (
                    (t.options.elementInViewport && (r = t.options.elementInViewport.getBoundingClientRect()),
                    (t.isElementInViewport = 0 <= r.bottom && 0 <= r.right && r.top <= v && r.left <= b),
                    e || t.isElementInViewport)
                  ) {
                    var l = Math.max(0, n),
                      s = Math.max(0, i + n),
                      c = Math.max(0, -n),
                      u = Math.max(0, n + i - v),
                      d = Math.max(0, i - (n + i - v)),
                      p = Math.max(0, -n + v - i),
                      m = 1 - (2 * (v - n)) / (v + i),
                      f = 1;
                    if (
                      (i < v ? (f = 1 - (c || u) / i) : s <= v ? (f = s / v) : d <= v && (f = d / v),
                      ('opacity' !== t.options.type && 'scale-opacity' !== t.options.type && 'scroll-opacity' !== t.options.type) ||
                        ((a.transform = 'translate3d(0,0,0)'), (a.opacity = f)),
                      'scale' === t.options.type || 'scale-opacity' === t.options.type)
                    ) {
                      var y = 1;
                      t.options.speed < 0 ? (y -= t.options.speed * f) : (y += t.options.speed * (1 - f)),
                        (a.transform = 'scale(' + y + ') translate3d(0,0,0)');
                    }
                    if ('scroll' === t.options.type || 'scroll-opacity' === t.options.type) {
                      var g = t.parallaxScrollDistance * m;
                      'absolute' === t.image.position && (g -= n), (a.transform = 'translate3d(0,' + g + 'px,0)');
                    }
                    t.css(t.image.$item, a),
                      t.options.onScroll &&
                        t.options.onScroll.call(t, {
                          section: o,
                          beforeTop: l,
                          beforeTopEnd: s,
                          afterTop: c,
                          beforeBottom: u,
                          beforeBottomEnd: d,
                          afterBottom: p,
                          visiblePercent: f,
                          fromViewportCenter: m
                        });
                  }
                }
              },
              {
                key: 'onResize',
                value: function () {
                  this.coverImage(), this.clipContainer();
                }
              }
            ]),
            u
          );
        })(),
        $ = function (e) {
          ('object' === ('undefined' == typeof HTMLElement ? 'undefined' : p(HTMLElement))
            ? e instanceof HTMLElement
            : e && 'object' === (void 0 === e ? 'undefined' : p(e)) && null !== e && 1 === e.nodeType && 'string' == typeof e.nodeName) &&
            (e = [e]);
          for (var t = arguments[1], o = Array.prototype.slice.call(arguments, 2), n = e.length, i = 0, a = void 0; i < n; i++)
            if (
              ('object' === (void 0 === t ? 'undefined' : p(t)) || void 0 === t
                ? e[i].jarallax || (e[i].jarallax = new w(e[i], t))
                : e[i].jarallax && (a = e[i].jarallax[t].apply(e[i].jarallax, o)),
              void 0 !== a)
            )
              return a;
          return e;
        };
      ($.constructor = w), (j.default = $);
    }).call(this, S(5));
  },
  function (e, t, o) {
    'use strict';
    var n = o(4),
      i =
        n.requestAnimationFrame ||
        n.webkitRequestAnimationFrame ||
        n.mozRequestAnimationFrame ||
        function (e) {
          var t = +new Date(),
            o = Math.max(0, 16 - (t - a)),
            n = setTimeout(e, o);
          return (a = t), n;
        },
      a = +new Date();
    var r = n.cancelAnimationFrame || n.webkitCancelAnimationFrame || n.mozCancelAnimationFrame || clearTimeout;
    Function.prototype.bind && ((i = i.bind(n)), (r = r.bind(n))), ((e.exports = i).cancel = r);
  }
]);

/*!
 * Name    : Elements Extension for Jarallax
 * Version : 1.0.0
 * Author  : nK <https://nkdev.info>
 * GitHub  : https://github.com/nk-o/jarallax
 */ !(function (n) {
  var o = {};
  function r(t) {
    if (o[t]) return o[t].exports;
    var e = (o[t] = { i: t, l: !1, exports: {} });
    return n[t].call(e.exports, e, e.exports, r), (e.l = !0), e.exports;
  }
  (r.m = n),
    (r.c = o),
    (r.d = function (t, e, n) {
      r.o(t, e) || Object.defineProperty(t, e, { enumerable: !0, get: n });
    }),
    (r.r = function (t) {
      'undefined' != typeof Symbol && Symbol.toStringTag && Object.defineProperty(t, Symbol.toStringTag, { value: 'Module' }),
        Object.defineProperty(t, '__esModule', { value: !0 });
    }),
    (r.t = function (e, t) {
      if ((1 & t && (e = r(e)), 8 & t)) return e;
      if (4 & t && 'object' == typeof e && e && e.__esModule) return e;
      var n = Object.create(null);
      if ((r.r(n), Object.defineProperty(n, 'default', { enumerable: !0, value: e }), 2 & t && 'string' != typeof e))
        for (var o in e)
          r.d(
            n,
            o,
            function (t) {
              return e[t];
            }.bind(null, o)
          );
      return n;
    }),
    (r.n = function (t) {
      var e =
        t && t.__esModule
          ? function () {
              return t.default;
            }
          : function () {
              return t;
            };
      return r.d(e, 'a', e), e;
    }),
    (r.o = function (t, e) {
      return Object.prototype.hasOwnProperty.call(t, e);
    }),
    (r.p = ''),
    r((r.s = 0));
})([
  function (t, e, n) {
    t.exports = n(1);
  },
  function (t, e, n) {
    'use strict';
    var o = r(n(2));
    function r(t) {
      return t && t.__esModule ? t : { default: t };
    }
    (0, r(n(3)).default)(),
      (0, o.default)(function () {
        'undefined' != typeof jarallax && jarallax(document.querySelectorAll('[data-jarallax-element]'));
      });
  },
  function (t, e, n) {
    'use strict';
    t.exports = function (t) {
      'complete' === document.readyState || 'interactive' === document.readyState
        ? t.call()
        : document.attachEvent
          ? document.attachEvent('onreadystatechange', function () {
              'interactive' === document.readyState && t.call();
            })
          : document.addEventListener && document.addEventListener('DOMContentLoaded', t);
    };
  },
  function (t, e, n) {
    'use strict';
    Object.defineProperty(e, '__esModule', { value: !0 }),
      (e.default = function () {
        var t = 0 < arguments.length && void 0 !== arguments[0] ? arguments[0] : i.default.jarallax;
        if (void 0 === t) return;
        var e = t.constructor;
        ['initImg', 'canInitParallax', 'init', 'destroy', 'clipContainer', 'coverImage', 'isVisible', 'onScroll', 'onResize'].forEach(
          function (p) {
            var f = e.prototype[p];
            e.prototype[p] = function () {
              var t = this,
                e = arguments || [];
              if (
                ('initImg' === p &&
                  null !== t.$item.getAttribute('data-jarallax-element') &&
                  ((t.options.type = 'element'),
                  (t.pureOptions.speed = t.$item.getAttribute('data-jarallax-element') || t.pureOptions.speed)),
                'element' !== t.options.type)
              )
                return f.apply(t, e);
              switch (((t.pureOptions.threshold = t.$item.getAttribute('data-threshold') || ''), p)) {
                case 'init':
                  var n = t.pureOptions.speed.split(' ');
                  (t.options.speed = t.pureOptions.speed || 0),
                    (t.options.speedY = n[0] ? parseFloat(n[0]) : 0),
                    (t.options.speedX = n[1] ? parseFloat(n[1]) : 0);
                  var o = t.pureOptions.threshold.split(' ');
                  (t.options.thresholdY = o[0] ? parseFloat(o[0]) : null), (t.options.thresholdX = o[1] ? parseFloat(o[1]) : null);
                  break;
                case 'onResize':
                  var r = t.css(t.$item, 'transform');
                  t.css(t.$item, { transform: '' });
                  var i = t.$item.getBoundingClientRect();
                  (t.itemData = { width: i.width, height: i.height, y: i.top + t.getWindowData().y, x: i.left }),
                    t.css(t.$item, { transform: r });
                  break;
                case 'onScroll':
                  var a = t.getWindowData(),
                    s = (a.y + a.height / 2 - t.itemData.y - t.itemData.height / 2) / (a.height / 2),
                    l = s * t.options.speedY,
                    u = s * t.options.speedX,
                    c = l,
                    d = u;
                  null !== t.options.thresholdY && l > t.options.thresholdY && (c = 0),
                    null !== t.options.thresholdX && u > t.options.thresholdX && (d = 0),
                    t.css(t.$item, { transform: 'translate3d(' + d + 'px,' + c + 'px,0)' });
                  break;
                case 'initImg':
                case 'isVisible':
                case 'clipContainer':
                case 'coverImage':
                  return !0;
              }
              return f.apply(t, e);
            };
          }
        );
      });
    var o,
      r = n(4),
      i = (o = r) && o.__esModule ? o : { default: o };
  },
  function (n, t, e) {
    'use strict';
    (function (t) {
      var e;
      (e = 'undefined' != typeof window ? window : void 0 !== t ? t : 'undefined' != typeof self ? self : {}), (n.exports = e);
    }).call(this, e(5));
  },
  function (t, e, n) {
    'use strict';
    var o,
      r =
        'function' == typeof Symbol && 'symbol' == typeof Symbol.iterator
          ? function (t) {
              return typeof t;
            }
          : function (t) {
              return t && 'function' == typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? 'symbol' : typeof t;
            };
    o = (function () {
      return this;
    })();
    try {
      o = o || Function('return this')() || (0, eval)('this');
    } catch (t) {
      'object' === ('undefined' == typeof window ? 'undefined' : r(window)) && (o = window);
    }
    t.exports = o;
  }
]);
