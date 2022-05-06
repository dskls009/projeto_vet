<template>
  <q-page padding class="full-width">
      <div class="text-h5">Filtros</div>
    <div class="row">
      <div class="col">
          <q-input outlined dense v-model="cpf" label="CPF" />
      </div>
      <div class="col">
        <q-input outlined dense v-model="nome" label="Nome" />
      </div>
      <div class="col">
        <q-input outlined dense v-model="sobrenome" label="Sobrenome" />
      </div>
    </div>
    
    <div class="row">
      <div class="col">
        <q-input outlined dense v-model="email" label="Email" />
      </div>
      <div class="col">
        <q-input outlined dense v-model="telefone" label="Telefone" />
      </div>
      <div class="col">
        
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-select
          outlined
          dense
          v-model="genero"
          :options="generos"
          label="Gênero"
          option-value="sigla"
          option-label="nome"
          emit-value
          map-options
          clearable
        />
      </div>
      <div class="col">
        <q-toggle v-model="inadimplente" label="Inadimplente" toggle-indeterminate/>
      </div>
      <div class="col">
        
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-table
          title="Clientes"
          :data="data"
          :columns="columns"
          :pagination.sync="pagination"
          :loading="loading"
          class="full-width"
          :rows-per-page-options="[0]"
          virtual-scroll
          binary-state-sort
          style="height: 400px; max-height: 800px;"
          separator="cell"
          dense
          flat
          bordered
          :visible-columns="colunasVisiveis"
        >
        <template v-slot:top>
          <div class="col-1 q-table__title">Clientes</div>
          
          <q-checkbox v-model="colunasVisiveis" val="cpf" label="CPF" />
          <q-checkbox v-model="colunasVisiveis" val="nome" label="Nome" />
          <q-checkbox v-model="colunasVisiveis" val="sobrenome" label="Sobrenome" />
          <q-checkbox v-model="colunasVisiveis" val="genero" label="Gênero" />
          <q-checkbox v-model="colunasVisiveis" val="email" label="Email" />
          <q-checkbox v-model="colunasVisiveis" val="telefone_1" label="Telefone (1)" />
          <q-checkbox v-model="colunasVisiveis" val="telefone_2" label="Telefone (2)" />
          <q-checkbox v-model="colunasVisiveis" val="inadimplente" label="Inadimplente" />
        </template>
          <template v-slot:body="props">
            <tr :props="props">
              <q-td :props="props" key="id"> {{ props.row.id }} </q-td>
              <q-td :props="props" key="cpf"> {{ props.row.cpf }} </q-td>
              <q-td :props="props" key="nome"> {{ props.row.nome }} </q-td>
              <q-td :props="props" key="sobrenome">
                {{ props.row.sobrenome }}
              </q-td>
              <q-td :props="props" key="genero"> {{ props.row.genero }} </q-td>
              <q-td :props="props" key="email"> {{ props.row.email }} </q-td>
              <q-td :props="props" key="telefone_1">
                {{ props.row.telefone_1 }}
              </q-td>
              <q-td :props="props" key="telefone_2">
                {{ props.row.telefone_2 }}
              </q-td>
              <q-td :props="props" key="inadimplente">
                {{ props.row.inadimplente ? 'Inadimplente' : '' }}
              </q-td>
            </tr>
          </template>
        </q-table>
      </div>
    </div>
    <div class="column items-end">
        <div class="col">
          <q-btn label="Exportar" color="green" flat icon="table_view" @click="excel_exportar" />
        </div>
      </div>
  </q-page>
</template>

<script>
import { defineComponent } from '@vue/composition-api';
import { cliente_relatorio, relatorio_download } from '../../services/relatorios/RelatorioService';

export default defineComponent({
  name: 'ClienteRelatorioView',
  data() {
    return {
      pagination: {
        sortBy: 'desc',
        descending: false,
        rowsPerPage: 0
      },
      generos: require('./../../assets/db/generos.json'),
      nome: null,
      sobrenome: null,
      cpf: null,
      email: null,
      telefone: null,
      inadimplente: null,
      genero: null,
      export: false,
      data: [],
      colunasVisiveis: ['id', 'cpf', 'nome', 'sobrenome', 'genero', 'email', 'telefone_1', 'telefone_2', 'inadimplente'],
      colunas: {
        col_id: null,
        col_cpf: null,
        col_nome: null,
        col_sobrenome: null,
        col_genero: null,
        col_email: null,
        col_telefone_1: null,
        col_telefone_2: null,
        col_inadimplente: null,
      },
      loading: false,
      pk: undefined,
      columns: [
        {
          name: 'id',
          label: 'ID',
          align: 'left',
          sortable: false
        },
        {
          name: 'cpf',
          label: 'CPF',
          align: 'left',
          sortable: false
        },
        {
          name: 'nome',
          label: 'Nome',
          align: 'left',
          sortable: true
        },
        {
          name: 'sobrenome',
          label: 'Sobrenome',
          align: 'left',
          sortable: true
        },
        {
          name: 'genero',
          label: 'Gênero',
          align: 'left',
          sortable: false
        },
        {
          name: 'email',
          label: 'Email',
          align: 'left',
          sortable: true
        },
        {
          name: 'telefone_1',
          label: 'Telefone (1)',
          align: 'left',
          sortable: false
        },
        {
          name: 'telefone_2',
          label: 'Telefone (2)',
          align: 'left',
          sortable: false
        },
        {
          name: 'inadimplente',
          label: 'Inadimplente',
          align: 'left',
          sortable: false
        }
      ]
    };
  },
  methods: {
    load: function() {
      cliente_relatorio(this);
    },
    excel_exportar: function(){
        for (let i = 0; i < this.colunasVisiveis.length; i++){
          switch (i){
            case 0:
              this.colunas.col_id = this.colunasVisiveis[i];
              break;
            case 1:
              this.colunas.col_cpf = this.colunasVisiveis[i];
              break;
            case 2:
              this.colunas.col_nome = this.colunasVisiveis[i];
              break;
            case 3:
              this.colunas.col_sobrenome = this.colunasVisiveis[i];
              break;
            case 4:
              this.colunas.col_genero = this.colunasVisiveis[i];
              break;
            case 5:
              this.colunas.col_email = this.colunasVisiveis[i];
              break;
            case 6:
              this.colunas.col_telefone_1 = this.colunasVisiveis[i];
              break;
            case 7:
              this.colunas.col_telefone_2 = this.colunasVisiveis[i];
              break;
            case 8:
              this.colunas.col_inadimplente = this.colunasVisiveis[i];
              break;
          }
        }
        relatorio_download(this)
        this.colunas.col_id = null
        this.colunas.col_cpf = null
        this.colunas.col_nome = null
        this.colunas.col_sobrenome = null
        this.colunas.col_genero = null
        this.colunas.col_email = null
        this.colunas.col_telefone_1 = null
        this.colunas.col_telefone_2 = null
        this.colunas.col_inadimplente = null
    }
  },
  mounted: function() {
    this.load();
  },
  watch: {
    nome: function() {
      this.load();
    },
    sobrenome: function() {
      this.load();
    },
    cpf: function() {
      this.load();
    },
    email: function() {
      this.load();
    },
    genero: function() {
      this.load();
    },
    telefone: function() {
      this.load();
    },
    inadimplente: function() {
      this.load();
    }
  }
});
</script>

<style>
.row {
  margin: 1px;
}
</style>
