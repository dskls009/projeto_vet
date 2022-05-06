import { SessionStorage, Notify } from 'quasar'
import { headers } from '../Service'


export function findall(vue){
    vue.$axios({
        method: 'GET',
        headers: headers(),
        url: `${vue.$servidor()}/veterinaria/condicao_especial`,
        params: {
            filtro: vue.filtro_condicao_especial,
            animal: vue.animal
        }
    }).then(response =>{
        vue.data_condicao_especial = response.data.data
        
    }).catch(error =>{
        vue.$erro(error)
    })
}

export function save(vue){
    let url = '/veterinaria/condicao_especial/create'
    if (vue.form_condicao && vue.form_condicao.id){
        url = `/veterinaria/condicao_especial/${vue.form_condicao.id}/edit`
    }
    vue.$axios({
        method: 'POST',
        headers: headers(),
        data: vue.form_condicao,
        url: vue.$servidor() + url
    }).then(response =>{

    }).catch(error =>{
        vue.$erro(error)
    })
}

export function erase(vue){
    let url = `/veterinaria/condicao_especial/${vue.pk}/delete`
    vue.$axios({
        method: 'DELETE',
        headers: headers(),
        url: vue.$servidor() + url
    }).then(response => {

    }).catch(error => {
        vue.$erro(error)
    })
}
