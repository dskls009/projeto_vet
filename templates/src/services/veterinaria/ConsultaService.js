import { SessionStorage, Notify } from 'quasar'
import { headers } from '../Service'


export function findall(vue){
    vue.$axios({
        method: 'GET',
        headers: headers(),
        url: `${vue.$servidor()}/veterinaria/consulta`,
        params: {
            filtro: vue.filtro,
            animal: vue.animal
        }
    }).then(response =>{
        vue.data = response.data.data
    }).catch(error =>{
        vue.$erro(error)
    })
}

export function get(vue){
    vue.$axios({
        method: 'GET',
        headers: headers(),
        url: `${vue.$servidor()}/veterinaria/consulta/${vue.pk}`,
    }).then(response =>{
        vue.form = response.data
    }).catch(error =>{
        vue.$erro(error)
    })
}

export function save(vue){
    let url = '/veterinaria/consulta/create'
    if (vue.form && vue.form.id){
        url = `/veterinaria/consulta/${vue.form.id}/edit`
    }
    vue.$axios({
        method: 'POST',
        headers: headers(),
        data: vue.form,
        url: vue.$servidor() + url
    }).then(response =>{
        if (response.data.status == true){
            vue.voltar_busca()
        }
    }).catch(error =>{
        vue.$erro(error)
        vue.$q.notify('Ocorreu um erro! Verifique os dados preenchidos!')
    })
}

export function erase(vue){
    let url = `/veterinaria/consulta/${vue.pk}/delete`
    vue.$axios({
        method: 'DELETE',
        headers: headers(),
        url: vue.$servidor() + url
    }).then(response => {

    }).catch(error => {
        vue.$erro(error)
    })
}
