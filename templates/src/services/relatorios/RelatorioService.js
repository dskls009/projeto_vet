import { SessionStorage, Notify, exportFile } from 'quasar'
import { headers } from '../Service'


export function cliente_relatorio(vue){
    vue.$axios({
        method: 'GET',
        headers: headers(),
        url: `${vue.$servidor()}/relatorios/cliente`,
        params: {
            nome: vue.nome,
            sobrenome: vue.sobrenome,
            cpf: vue.cpf,
            email: vue.email,
            telefone: vue.telefone,
            inadimplente: vue.inadimplente,
            col_id: vue.colunas.col_id,
            col_cpf: vue.colunas.col_cpf,
            col_nome: vue.colunas.col_nome,
            col_sobrenome: vue.colunas.col_sobrenome,
            col_genero: vue.colunas.col_genero,
            col_email: vue.colunas.col_email,
            col_telefone_1: vue.colunas.col_telefone_1,
            col_telefone_2: vue.colunas.col_telefone_2,
            col_inadimplente: vue.colunas.col_inadimplente,
            genero: vue.genero,
            export: false
        }
    }).then(response =>{
        vue.data = response.data.data
    }).catch(error =>{
        vue.$erro(error)
    })
}

export function relatorio_download(vue){
    vue.$axios({
        method: 'GET',
        headers: headers(),
        url: `${vue.$servidor()}/relatorios/cliente`,
        responseType: 'blob',
        params: {
            nome: vue.nome,
            sobrenome: vue.sobrenome,
            cpf: vue.cpf,
            email: vue.email,
            telefone: vue.telefone,
            inadimplente: vue.inadimplente,
            col_id: vue.colunas.col_id,
            col_cpf: vue.colunas.col_cpf,
            col_nome: vue.colunas.col_nome,
            col_sobrenome: vue.colunas.col_sobrenome,
            col_genero: vue.colunas.col_genero,
            col_email: vue.colunas.col_email,
            col_telefone_1: vue.colunas.col_telefone_1,
            col_telefone_2: vue.colunas.col_telefone_2,
            col_inadimplente: vue.colunas.col_inadimplente,
            genero: vue.genero,
            export: true
        }
    }).then(response =>{
        exportFile('report.pdf', response.data)
    }).catch(error =>{
        vue.$erro(error)
    })
}

export function animal_relatorio(vue){
    vue.$axios({
        method: 'GET',
        headers: headers(),
        url: `${vue.$servidor()}/relatorios/animal`,
        params: {
            cliente__nome: vue.cliente__nome,
            cliente__sobrenome: vue.cliente__sobrenome,
            cliente__cpf: vue.cliente__cpf,
            cliente__inadimplente: vue.cliente__inadimplente,
            rga: vue.rga,
            nome: vue.nome,
            especie: vue.especie,
            raca: vue.raca,
            cor: vue.cor,
            peso: vue.peso,
            porte: vue.porte,
            castrado: vue.castrado,
            data_castracao_de: vue.data_castracao_de,
            data_castracao_ate: vue.data_castracao_ate,
            sexo: vue.sexo,
            col_id: vue.colunas.col_id,
            col_cliente__cpf: vue.colunas.col_cliente__cpf,
            col_cliente__nome: vue.colunas.col_cliente__nome,
            col_cliente__sobrenome: vue.colunas.col_cliente__sobrenome,
            col_cliente__inadimplente: vue.colunas.col_cliente__inadimplente,
            col_rga: vue.colunas.col_rga,
            col_nome: vue.colunas.col_nome,
            col_especie: vue.colunas.col_especie,
            col_raca: vue.colunas.col_raca,
            col_cor: vue.colunas.col_cor,
            col_peso: vue.colunas.col_peso,
            col_porte: vue.colunas.col_porte,
            col_sexo: vue.colunas.col_sexo,
            col_castrado: vue.colunas.col_castrado,
            col_data_castracao: vue.colunas.col_data_castracao,
            export: vue.export
        }
    }).then(response =>{
        vue.data = response.data.data
    }).catch(error =>{
        vue.$erro(error)
    })
}