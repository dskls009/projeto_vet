import { SessionStorage, Notify, exportFile } from 'quasar';
import { headers } from '../Service';

export function findall(vue) {
  vue
    .$axios({
      method: 'GET',
      headers: headers(),
      url: `${vue.$servidor()}/base64`,
      params: {
        filtro: vue.filtro
      }
    })
    .then(response => {
      vue.data = response.data.data;
    })
    .catch(error => {
      vue.$erro(error);
    });
}

export function download(vue) {
  vue
    .$axios({
      method: 'GET',
      headers: headers(),
      url: `${vue.$servidor()}/base64/${vue.pk}/download`,
      responseType: 'blob'
    })
    .then(response => {
      let headerLine = response.headers['content-disposition'];
      let nome = headerLine.substring(headerLine.indexOf('"') + 1, headerLine.lastIndexOf('"'))
      
      exportFile(nome, response.data)
    })
    .catch(error => {
      vue.$erro(error);
    });
}

export function get(vue) {
  vue
    .$axios({
      method: 'GET',
      headers: headers(),
      url: `${vue.$servidor()}/base64/${vue.pk}`
    })
    .then(response => {
      vue.form = response.data;
    })
    .catch(error => {
      vue.$erro(error);
    });
}

export function save(vue) {
  let url = '/base64/create';
  if (vue.form && vue.form.id) {
    url = `/base64/${vue.form.id}/edit`;
  }
  vue
    .$axios({
      method: 'POST',
      headers: headers(),
      data: vue.base64,
      url: vue.$servidor() + url
    })
    .then(response => {
      if (response.data.status == true) {
        vue.base64__id = response.data.base64__id;
      }
    })
    .catch(error => {
      vue.$erro(error);
      vue.$q.notify('Ocorreu um erro! Verifique os dados preenchidos!');
    });
}

export function erase(vue) {
  let url = `/base64/${vue.pk}/delete`;
  vue
    .$axios({
      method: 'DELETE',
      headers: headers(),
      url: vue.$servidor() + url
    })
    .then(response => {})
    .catch(error => {
      vue.$erro(error);
    });
}
