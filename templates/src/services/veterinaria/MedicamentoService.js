import { SessionStorage, Notify } from 'quasar'
import { headers } from '../Service'


export function findall(vue){
    vue.$axios({
        method: 'GET',
        headers: headers(),
        url: `${vue.$servidor()}/veterinaria/medicamento`,
        params: {
            filtro: vue.filtro,
        }
    }).then(response =>{
        vue.data = response.data.data
        vue.data_medicamento = response.data.data
    }).catch(error =>{
        vue.$erro(error)
    })
}

export function get(vue){
    vue.$axios({
        method: 'GET',
        headers: headers(),
        url: `${vue.$servidor()}/veterinaria/medicamento/${vue.pk}`,
    }).then(response =>{
        vue.form = response.data
    }).catch(error =>{
        vue.$erro(error)
    })
}

export function save(vue){
    let url = '/veterinaria/medicamento/create'
    if (vue.form && vue.form.id){
        url = `/veterinaria/medicamento/${vue.form.id}/edit`
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
    })
}

export function erase(vue){
    let url = `/veterinaria/medicamento/${vue.pk}/delete`
    vue.$axios({
        method: 'DELETE',
        headers: headers(),
        url: vue.$servidor() + url
    }).then(response => {

    }).catch(error => {
        vue.$erro(error)
    })
}
