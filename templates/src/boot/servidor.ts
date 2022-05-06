import { boot } from 'quasar/wrappers';

export default boot(({ Vue }) => {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
  Vue.prototype.$servidor = function server():string {
    let a:string = 'http://' + window.location.host + '/api';
    if (a === 'http:///api' || a === 'http://api') {
      a = 'http://localhost:8000/api'
    }
    if (location.protocol === 'https:') {
      a = a.replace('http', 'https')
    }
    if (a.indexOf('8080') >= 0) {
      a = a.replace('8080', '8000')
    }
    return a
  };
});