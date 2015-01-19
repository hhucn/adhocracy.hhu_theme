from fanstatic import Library, Group, Resource
# external libraries
from js.jquery import jquery
from js.jquery_joyride import joyride
from js.socialshareprivacy import socialshareprivacy


# --[ twitter bootstrap ]---------------------------------------------------

bootstrap_library = Library('bootstrap', 'bootstrap', version="2.1.1")
bootstrap_js = Resource(bootstrap_library, 'js/bootstrap.js',
                        minified='js/bootstrap.min.js',
                        depends=[jquery])
yaml_base = Resource(bootstrap_library, 'yaml/core/base.css')
yaml_print = Resource(bootstrap_library, 'yaml/print/print_draft.css',
                      depends=[yaml_base])
bootstrap_css = Resource(bootstrap_library, 'css/bootstrap.css',
                         minified='css/bootstrap.min.css',
                         depends=[yaml_base])  # include it after yaml
bootstrap = Group([bootstrap_js, yaml_base, yaml_print, bootstrap_css])


# --[ stylesheets ]---------------------------------------------------------

stylesheets_library = Library('stylesheets', 'stylesheets')
fonts = Resource(stylesheets_library, 'screen/fonts.css',
                 depends=[bootstrap_css])
basemod = Resource(stylesheets_library, 'screen/basemod.css',
                   depends=[fonts])
content = Resource(stylesheets_library, 'screen/content.css',
                   depends=[basemod])
style = Resource(stylesheets_library, 'style.css',
                 depends=[content])
stylesheets = Group([fonts, basemod, content, style])

# --[ jquery.autocomplete ]-------------------------------------------------

autocomplete_library = Library('autocomplete', 'javascripts', version="1.2.2")
autocomplete_js = Resource(autocomplete_library, 'jquery.autocomplete.min.js',
                           depends=[jquery])
autocomplete_css = Resource(autocomplete_library, 'jquery.autocomplete.css')
autocomplete = Group([autocomplete_js, autocomplete_css])


# --[ other versioned libraries ]-------------------------------------------

placeholder_library = Library('placeholder', 'javascripts', version="2.0.7")
placeholder = Resource(placeholder_library, 'jquery.placeholder.js',
                       minified='jquery.placeholder.min.js',
                       depends=[jquery])

jquerytools_library = Library('jquerytools', 'javascripts', version="1.2.7")
jquerytools = Resource(jquerytools_library, 'jquery.tools.min.js',
                       depends=[jquery])

# --[ misc javascripts ]----------------------------------------------------

misc_library = Library('misc', 'javascripts')
elastic = Resource(misc_library, 'jquery.elastic.js',
                   depends=[jquery])
cycle = Resource(misc_library, 'jquery.multipleelements.cycle.min.js',
                 depends=[jquery])
modernizr = Resource(misc_library, 'modernizr.js',
                     depends=[jquery])
spectrum_css = Resource(misc_library, 'spectrum/spectrum.css')
spectrum = Resource(misc_library, 'spectrum/spectrum.js',
                    minified='spectrum/spectrum.min.js',
                    depends=[jquery, spectrum_css])
openid_selector = Resource(misc_library, 'openid.js',
                           depends=[jquery])

# --[ adhocracy ]-----------------------------------------------------------

adhocracy_library = Library('adhocracy', 'javascripts')
adhocracy = Resource(adhocracy_library, 'adhocracy.js',
                     depends=[jquery, bootstrap_js, elastic,
                              placeholder, modernizr, jquerytools,
                              openid_selector])


# --[ knockout ]------------------------------------------------------------

knockout_library = Library('knockoutjs', 'javascripts')
knockout_js = Resource(knockout_library, 'knockout.debug.js',
                       minified='knockout.js',
                       depends=[jquery])
knockout_mapping_js = Resource(knockout_library, 'knockout.mapping.debug.js',
                               minified='knockout.mapping.js',
                               depends=[knockout_js])
knockout = Group([knockout_js, knockout_mapping_js])
adhocracy_ko = Resource(knockout_library, 'adhocracy.ko.js',
                        depends=[adhocracy, knockout])

# --[ moment ]-------------------------------------------------------------

moment_library = Library('moment', 'javascripts/moment', version="2.7.0")
moment = Resource(moment_library, 'moment.js',
                  minified='moment.min.js')
js_i18n['moment'] = dict()
for _locale in LOCALES:
    moment_path = os.path.join(static_path, 'javascripts', 'moment')
    for locale in (str(_locale), _locale.language):
        filename = locale.lower().replace('_', '-') + '.js'
        if locale not in js_i18n['moment']:
            if os.path.exists(os.path.join(moment_path, filename)):
                js_i18n['moment'][locale] = Resource(
                    moment_library, filename, depends=[moment])

