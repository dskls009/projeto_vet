<template>
  <q-page padding class="full-width">
      <div class="text-h5">Filtros do Cliente</div>
    <div class="row">
      <div class="col">
          <q-input outlined dense v-model="cliente__cpf" label="CPF" />
      </div>
      <div class="col">
        <q-input outlined dense v-model="cliente__nome" label="Nome" />
      </div>
      <div class="col">
        <q-input outlined dense v-model="cliente__sobrenome" label="Sobrenome" />
      </div>
      <div class="col">
        <q-toggle v-model="cliente__inadimplente" label="Inadimplente" toggle-indeterminate/>
      </div>
    </div>
    <div class="text-h5">Filtros do Animal</div>
    <div class="row">
      <div class="col">
        <q-input outlined dense v-model="rga" label="RGA" />
      </div>
      <div class="col">
        <q-input outlined dense v-model="nome" label="Nome" />
      </div>
      <div class="col">
        <q-select
          outlined
          dense
          v-model="sexo"
          :options="sexos"
          label="Sexo"
          option-value="sigla"
          option-label="nome"
          emit-value
          map-options
          clearable
        />
      </div>
      <div class="col">
        <q-input outlined dense v-model="peso" label="Peso" />
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-input outlined dense v-model="especie" label="Espécie" />
      </div>
      <div class="col">
        <q-input outlined dense v-model="raca" label="Raça" />
      </div>
      <div class="col">
        <q-input outlined dense v-model="cor" label="Cor" />
      </div>
      <div class="col">
        <q-input outlined dense v-model="porte" label="Porte" />
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-toggle v-model="castrado" label="Castrado" toggle-indeterminate/>
      </div>
      <div class="col">
        <q-input outlined dense v-model="data_castracao_de" label="Data de Castração (de)" />
      </div>
      <div class="col">
        <q-input outlined dense v-model="data_castracao_ate" label="Data de Castração (até)" />
      </div>
    </div>
    <div class="row">
      <div class="col">
        <q-table
          title="Animais"
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
          <div class="col-2 q-table__title">Animais</div>
          <div>
              Colunas do Cliente
          <q-checkbox v-model="colunasVisiveis" val="cliente__cpf" label="CPF" />
          <q-checkbox v-model="colunasVisiveis" val="cliente__nome" label="Nome" />
          <q-checkbox v-model="colunasVisiveis" val="cliente__sobrenome" label="Sobrenome" />
          <q-checkbox v-model="colunasVisiveis" val="cliente__inadimplente" label="Inadimplente" />
          </div>
          <div>
              Colunas do Animal
          <q-checkbox v-model="colunasVisiveis" val="rga" label="RGA" />
          <q-checkbox v-model="colunasVisiveis" val="nome" label="Nome" />
          <q-checkbox v-model="colunasVisiveis" val="especie" label="Espécie" />
          <q-checkbox v-model="colunasVisiveis" val="raca" label="Raça" />
          <q-checkbox v-model="colunasVisiveis" val="cor" label="Cor" />
          <q-checkbox v-model="colunasVisiveis" val="peso" label="Peso" />
          <q-checkbox v-model="colunasVisiveis" val="porte" label="Porte" />
          <q-checkbox v-model="colunasVisiveis" val="sexo" label="Sexo" />
          <q-checkbox v-model="colunasVisiveis" val="castrado" label="Castrado" />
          <q-checkbox v-model="colunasVisiveis" val="data_castracao" label="Data de Castração" />
          </div>
        </template>
          <template v-slot:body="props">
            <tr :props="props">
              <q-td :props="props" key="id"> {{ props.row.id }} </q-td>
              <q-td :props="props" key="cliente__cpf"> {{ props.row.cliente__cpf }} </q-td>
              <q-td :props="props" key="cliente__nome"> {{ props.row.cliente__nome }} </q-td>
              <q-td :props="props" key="cliente__sobrenome">
                {{ props.row.cliente__sobrenome }}
              </q-td>
              <q-td :props="props" key="cliente__inadimplente">
                {{ props.row.cliente__inadimplente ? 'Inadimplente' : '' }}
              </q-td>
              <q-td :props="props" key="rga"> {{ props.row.rga }} </q-td>
              <q-td :props="props" key="nome"> {{ props.row.nome }} </q-td>
              <q-td :props="props" key="especie"> {{ props.row.especie }} </q-td>
              <q-td :props="props" key="raca">
                {{ props.row.raca }}
              </q-td>
              <q-td :props="props" key="cor">
                {{ props.row.cor }}
              </q-td>
              <q-td :props="props" key="peso"> {{ props.row.peso }} </q-td>
              <q-td :props="props" key="porte"> {{ props.row.porte }} </q-td>
              <q-td :props="props" key="sexo"> {{ props.row.sexo }} </q-td>
              <q-td :props="props" key="castrado">
                {{ props.row.castrado ? "Castrado" : "" }}
              </q-td>
              <q-td :props="props" key="data_castracao">
                {{ arrumar_data(props.row.data_castracao) }}
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
import { animal_relatorio } from '../../services/relatorios/RelatorioService';

export default defineComponent({
  name: 'AnimalRelatorioView',
  data() {
    return {
      pagination: {
        sortBy: 'desc',
        descending: false,
        rowsPerPage: 0
      },
      sexos: require('./../../assets/db/sexos.json'),
      cliente__nome: null,
      cliente__sobrenome: null,
      cliente__cpf: null,
      cliente__inadimplente: null,
      nome: null,
      rga: null,
      especie: null,
      raca: null,
      cor: null,
      peso: null,
      porte: null,
      castrado: null,
      data_castracao_de: null,
      data_castracao_ate: null,
      sexo: null,
      export: false,
      data: [],
      colunasVisiveis: ['id', 'cliente__cpf', 'cliente__nome', 'cliente__sobrenome', 'cliente__inadimplente', 'rga', 'nome', 'especie', 'raca', 'cor', 'peso', 'porte', 'castrado', 'data_castracao', 'sexo'],
      colunas: {
        col_id: null,
        col_cliente__cpf: null,
        col_cliente__nome: null,
        col_cliente__sobrenome: null,
        col_cliente__inadimplente: null,
        col_rga: null,
        col_nome: null,
        col_especie: null,
        col_raca: null,
        col_cor: null,
        col_peso: null,
        col_porte: null,
        col_sexo: null,
        col_castrado: null,
        col_data_castracao: null,
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
          name: 'cliente__cpf',
          label: 'CPF',
          align: 'left',
          sortable: false
        },
        {
          name: 'cliente__nome',
          label: 'Nome',
          align: 'left',
          sortable: true
        },
        {
          name: 'cliente__sobrenome',
          label: 'Sobrenome',
          align: 'left',
          sortable: true
        },
        {
          name: 'cliente__inadimplente',
          label: 'Inadimplente',
          align: 'left',
          sortable: false
        },
        {
          name: 'rga',
          label: 'RGA',
          align: 'left',
          sortable: false
        },
        {
          name: 'nome',
          label: 'Nome',
          align: 'left',
          sortable: false
        },
        {
          name: 'especie',
          label: 'Espécie',
          align: 'left',
          sortable: false
        },
        {
          name: 'raca',
          label: 'Raça',
          align: 'left',
          sortable: false
        },
        {
          name: 'cor',
          label: 'Cor',
          align: 'left',
          sortable: false
        },
        {
          name: 'peso',
          label: 'Peso',
          align: 'left',
          sortable: false
        },
        {
          name: 'porte',
          label: 'Porte',
          align: 'left',
          sortable: false
        },
        {
          name: 'castrado',
          label: 'Castrado',
          align: 'left',
          sortable: false
        },
        {
          name: 'data_castracao',
          label: 'Data de Castração',
          align: 'left',
          sortable: false
        }
      ]
    };
  },
  methods: {
    load: function() {
      animal_relatorio(this);
    },
    excel_exportar: function(){
        for (let i = 0; i < this.colunasVisiveis.length; i++){
          switch (i){
            case 0:
              this.colunas.col_id = this.colunasVisiveis[i];
              break;
            case 1:
              this.colunas.col_cliente__cpf = this.colunasVisiveis[i];
              break;
            case 2:
              this.colunas.col_cliente__nome = this.colunasVisiveis[i];
              break;
            case 3:
              this.colunas.col_cliente__sobrenome = this.colunasVisiveis[i];
              break;
            case 4:
              this.colunas.col_cliente__inadimplente = this.colunasVisiveis[i];
              break;
            case 5:
              this.colunas.col_rga = this.colunasVisiveis[i];
              break;
            case 6:
              this.colunas.col_nome = this.colunasVisiveis[i];
              break;
            case 7:
              this.colunas.col_especie = this.colunasVisiveis[i];
              break;
            case 8:
              this.colunas.col_raca = this.colunasVisiveis[i];
              break;
            case 9:
              this.colunas.col_cor = this.colunasVisiveis[i];
              break;
            case 10:
              this.colunas.col_peso = this.colunasVisiveis[i];
              break;
            case 11:
              this.colunas.col_porte = this.colunasVisiveis[i];
              break;
            case 12:
              this.colunas.col_sexo = this.colunasVisiveis[i];
              break;
            case 13:
              this.colunas.col_castrado = this.colunasVisiveis[i];
              break;
            case 14:
              this.colunas.col_data_castracao = this.colunasVisiveis[i];
              break;
          }
        }
        this.export = true;
        this.load();
        this.export = false;
    },
    arrumar_data: function(date){
      if (date != null && date != undefined){
        let data = date[0].split('-')
        let dh_format = data[2]+'/'+data[1]+'/'+data[0]
        return dh_format
      } else {
        return ''
      }
    }
  },
  mounted: function() {
    this.load();
  },
  watch: {
    cliente__nome: function() {
      this.load();
    },
    cliente__sobrenome: function() {
      this.load();
    },
    cliente__cpf: function() {
      this.load();
    },
    cliente__inadimplente: function() {
      this.load();
    },
    rga: function() {
      this.load();
    },
    nome: function() {
      this.load();
    },
    especie: function() {
      this.load();
    },
    raca: function() {
      this.load();
    },
    cor: function() {
      this.load();
    },
    peso: function() {
      this.load();
    },
    porte: function() {
      this.load();
    },
    sexo: function() {
      this.load();
    },
    castrado: function() {
      this.load();
    },
    data_castracao_de: function() {
      this.load();
    },
    data_castracao_ate: function() {
      this.load();
    },
  }
});
</script>

<style>
.row {
  margin: 1px;
}
</style>
