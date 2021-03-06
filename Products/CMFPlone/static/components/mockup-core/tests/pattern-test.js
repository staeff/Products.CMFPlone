// Tests for the Mockup Base Pattern
define([
  'expect',
  'sinon',
  'jquery',
  'pat-registry',
  'mockup-patterns-base'
], function(expect, sinon, $, Registry, Base) {
  'use strict';
  window.mocha.setup('bdd');

  describe('The Mockup Base Pattern', function () {

    beforeEach(function() {
      this.jqueryPatterns = {};
      $.each(Registry.patterns, $.proxy(function(patternName) {
        this.jqueryPatterns[Registry.patterns[patternName].prototype.jqueryPlugin] =
            $.fn[Registry.patterns[patternName].prototype.jqueryPlugin];

        $.fn[Registry.patterns[patternName].prototype.jqueryPlugin] = undefined;
      }, this));
      this._patterns = Registry.patterns;
      Registry.patterns = {};
    });
    afterEach(function() {
      var jqueryPlugin;
      $.each(Registry.patterns, function(patternName) {
        $.fn[Registry.patterns[patternName].prototype.jqueryPlugin] = undefined;
      });
      Registry.patterns = this._patterns;
      $.each(Registry.patterns, $.proxy(function(patternName) {
        jqueryPlugin = Registry.patterns[patternName].prototype.jqueryPlugin;
        $.fn[jqueryPlugin] = this.jqueryPatterns[jqueryPlugin];
      }, this));
    });

    it('can be extended and used in similar way as classes', function(done) {
      var Tmp = Base.extend({
        name: 'example',
        trigger: 'pat-example',
        some: 'thing',
        init: function() {
          expect(this.$el.hasClass('pat-example')).to.equal(true);
          expect(this.options).to.have.keys(['option']);
          this.extra();
        },
        extra: function() {
          expect(this.some).to.equal('thing');
          done();
        }
      });
      var tmp = new Tmp($('<div class="pat-example"/>'), {option: 'value'});
    });

    it('will automatically register a pattern in the Patternslib registry when extended', function() {
      var registerSpy = sinon.spy();
      var originalRegister = Registry.register;
      Registry.register = function (pattern, name) {
        registerSpy();
        originalRegister(pattern, name);
      };
      var NewPattern = Base.extend({
        name: 'example',
        trigger: '.pat-example'
      });
      expect(NewPattern.trigger).to.be.equal('.pat-example');
      expect(Object.keys(Registry.patterns).length).to.be.equal(1);
      expect(Object.keys(Registry.patterns)[0]).to.be.equal('example');
      expect(registerSpy.called).to.be.equal(true);
      Registry.register = originalRegister;
    });

    it('will not automatically register a pattern without a "name" attribute', function() {
      var registerSpy = sinon.spy();
      var originalRegister = Registry.register;
      Registry.register = function (pattern, name) {
        registerSpy();
        originalRegister(pattern, name);
      };
      var NewPattern = Base.extend({trigger: '.pat-example'});
      expect(registerSpy.called).to.be.equal(false);
      Registry.register = originalRegister;
    });

    it('will not automatically register a pattern without a "trigger" attribute', function() {
      var registerSpy = sinon.spy();
      var originalRegister = Registry.register;
      Registry.register = function (pattern, name) {
        registerSpy();
        originalRegister(pattern, name);
      };
      var NewPattern = Base.extend({name: 'example'});
      expect(registerSpy.called).to.be.equal(false);
      Registry.register = originalRegister;
    });

    it('will instantiate new instances of a pattern when the DOM is scanned', function(done) {
      var NewPattern = Base.extend({
        name: 'example',
        trigger: '.pat-example',
        init: function() {
          expect(this.$el.attr('class')).to.be.equal('pat-example');
          done();
        }
      });
      Registry.scan($('<div class="pat-example"/>'));
    });

    it('requires that patterns that extend it provide an object of properties', function() {
      expect(Base.extend.bind(Base, {})).should.assert("Pattern configuration properties required when calling Base.extend");
    });

    it('can be extended multiple times', function(done) {
      var Tmp1 = Base.extend({
        name: 'thing',
        trigger: 'pat-thing',
        something: 'else',
        init: function() {
          expect(this.some).to.equal('thing3');
          expect(this.something).to.equal('else');
          done();
        }
      });
      var Tmp2 = Tmp1.extend({
        name: 'thing',
        trigger: 'pat-thing',
        some: 'thing2',
        init: function() {
          expect(this.some).to.equal('thing3');
          expect(this.something).to.equal('else');
          this.constructor.__super__.constructor.__super__.init.call(this);
        }
      });
      var Tmp3 = Tmp2.extend({
        name: 'thing',
        trigger: 'pat-thing',
        some: 'thing3',
        init: function() {
          expect(this.some).to.equal('thing3');
          expect(this.something).to.equal('else');
          this.constructor.__super__.init.call(this);
        }
      });
      var tmp3 = new Tmp3('element', {option: 'value'});
    });

    it('has on/emit helpers to prefix events', function(done) {
      var Tmp = Base.extend({
        name: 'tmp',
        trigger: '.pat-tmp',
        init: function() {
          this.on('something', function(e, arg1) {
            expect(arg1).to.be('yaay!');
            done();
          });
          this.emit('somethingelse', ['yaay!']);
        }
      });
      var tmp = new Tmp(
        $('<div/>').on('somethingelse.tmp.patterns', function(e, arg1) {
          $(this).trigger('something.tmp.patterns', [arg1]);
          done();
        }));
    });
  });
});
