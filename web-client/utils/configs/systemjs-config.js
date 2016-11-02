SystemJS.config({
 transpiler: 'plugin-babel',
 map: {
  'plugin-babel': 
  '../../node_modules/systemjs-plugin-babel/plugin-babel.js',
  'systemjs-babel-build': 
  '../../node_modules/systemjs-plugin-babel/systemjs-babel-browser.js',

  'main': '../../app.js'
 }
});