<template>
  <q-page padding class="full-width">
    <div class="column items-end">
      <div class="col">
        <q-btn
          label="Buscar Cliente"
          flat
          color="negative"
          icon="arrow_back"
          @click="buscar_cliente"
        />
        <q-btn
          label="Cadastrar Doença"
          flat
          icon-right="coronavirus"
          @click="cadastrar_doenca"
        />
        <q-btn
          label="Cadastrar Medicamento"
          flat
          icon-right="medication"
          @click="cadastrar_medicamento"
        />
        <q-btn
          label="Cadastrar Cliente"
          flat
          icon-right="person"
          @click="cadastrar_cliente"
        />
        <q-btn
          label="Cadastrar Animal"
          flat
          icon-right="pets"
          @click="cadastrar_animal"
        />
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
        >
          <template v-slot:top-right>
            <q-input
              outlined
              dense
              debounce="300"
              v-model="filtro"
              @input="load"
            >
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
          </template>
          <template v-slot:body="props">
            <tr :props="props">
              <q-td :props="props" key="id"
                ><q-btn
                  size="sm"
                  dense
                  icon="edit"
                  flat
                  color="primary"
                  rounded
                  @click="$router.push(`/animal/edicao/${props.row.id}`)"
                />
                <q-btn
                  size="sm"
                  dense
                  icon="delete"
                  flat
                  color="negative"
                  rounded
                  @click="erase(props.row)"
                />
                </q-td>
              <q-td :props="props" key="cliente__cpf">
                {{ props.row.cliente__cpf }}</q-td
              >
              <q-td :props="props" key="rga">{{ props.row.rga }} </q-td>
              <q-td :props="props" key="nome">{{ props.row.nome }} </q-td>
              <q-td :props="props" key="sexo">{{ props.row.sexo }} </q-td>
              <q-td :props="props" key="especie">{{ props.row.especie }} </q-td>
              <q-td :props="props" key="raca">{{ props.row.raca }} </q-td>
              <q-td :props="props" key="cor">{{ props.row.cor }} </q-td>
              <q-td :props="props" key="peso">{{ props.row.peso }} </q-td>
              <q-td :props="props" key="porte">{{ props.row.porte }} </q-td>
              <q-td :props="props" key="castrado">
                {{ props.row.castrado ? 'Castrado' : '' }}
              </q-td>
              <q-td :props="props" key="data_castracao">
                {{ arrumar_data(props.row.data_castracao) }}
              </q-td>
              <q-td :props="props" key="atendimento">
                <q-btn
                  size="sm"
                  dense
                  icon="search"
                  flat
                  color="primary"
                  rounded
                  @click="buscar_atendimento(props.row.id)"
                ></q-btn>
                <q-btn
                  size="sm"
                  dense
                  icon="add"
                  flat
                  color="primary"
                  rounded
                  @click="registrar_atendimento(props.row.id)"
                ></q-btn>
              </q-td>
              <q-td :props="props" key="consulta">
                <q-btn
                  size="sm"
                  dense
                  icon="search"
                  flat
                  color="primary"
                  rounded
                  @click="buscar_consulta(props.row.id)"
                ></q-btn>
                <q-btn
                  size="sm"
                  dense
                  icon="add"
                  flat
                  color="primary"
                  rounded
                  @click="registrar_consulta(props.row.id)"
                ></q-btn>
              </q-td>
              <q-td :props="props" key="cirurgia">
                <q-btn
                  size="sm"
                  dense
                  icon="search"
                  flat
                  color="primary"
                  rounded
                  @click="buscar_cirurgia(props.row.id)"
                ></q-btn>
                <q-btn
                  size="sm"
                  dense
                  icon="add"
                  flat
                  color="primary"
                  rounded
                  @click="registrar_cirurgia(props.row.id)"
                ></q-btn>
              </q-td>
              <q-td :props="props" key="emergencia">
                <q-btn
                  size="sm"
                  dense
                  icon="search"
                  flat
                  color="primary"
                  rounded
                  @click="buscar_emergencia(props.row.id)"
                ></q-btn>
                <q-btn
                  size="sm"
                  dense
                  icon="add"
                  flat
                  color="primary"
                  rounded
                  @click="registrar_emergencia(props.row.id)"
                ></q-btn>
              </q-td>
              <q-td :props="props" key="vacina"
                >
                <q-btn
                  size="sm"
                  dense
                  icon="search"
                  flat
                  color="primary"
                  rounded
                  @click="buscar_vacina(props.row.id)"
                ></q-btn>
                <q-btn
                  size="sm"
                  dense
                  icon="add"
                  flat
                  color="primary"
                  rounded
                  @click="registrar_vacina(props.row.id)"
                ></q-btn>
              </q-td>
            </tr>
          </template>
        </q-table>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from '@vue/composition-api';
import { findall, erase } from '../../services/commons/AnimalService';
import { SessionStorage } from 'quasar';

export default defineComponent({
  name: 'AnimalBuscaView',
  data() {
    return {
      filtro: undefined,
      pagination: {
        sortBy: 'desc',
        descending: false,
        rowsPerPage: 0
      },
      data: [],
      loading: false,
      pk: undefined,
      columns: [
        {
          name: 'id',
          label: 'Ações',
          align: 'center',
          sortable: false
        },
        {
          name: 'cliente__cpf',
          label: 'Tutor CPF',
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
          sortable: true
        },
        {
          name: 'sexo',
          label: 'Sexo',
          align: 'left',
          sortable: true
        },
        {
          name: 'especie',
          label: 'Espécie',
          align: 'left',
          sortable: true
        },
        {
          name: 'raca',
          label: 'Raça',
          align: 'left',
          sortable: true
        },
        {
          name: 'cor',
          label: 'Cor',
          align: 'left',
          sortable: true
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
          sortable: true
        },
        {
          name: 'castrado',
          label: 'Castrado',
          align: 'left',
          sortable: true
        },
        {
          name: 'data_castracao',
          label: 'Data de Castração',
          align: 'left',
          sortable: true
        },
        {
          name: 'atendimento',
          label: 'Atendimentos',
          align: 'center',
          sortable: false
        },
        {
          name: 'consulta',
          label: 'Consultas',
          align: 'center',
          sortable: false
        },
        {
          name: 'cirurgia',
          label: 'Cirurgias',
          align: 'center',
          sortable: false
        },
        {
          name: 'emergencia',
          label: 'Emergências',
          align: 'center',
          sortable: false
        },
        {
          name: 'vacina',
          label: 'Vacinas',
          align: 'center',
          sortable: false
        }
      ],
      cliente: undefined
    };
  },
  methods: {
    load: function() {
      findall(this);
    },
    erase: function (row) {
      this.$q
        .bottomSheet({
          message: 'Deseja apagar realmente este registro?',
          actions: [
            {
              label: 'Sim',
              id: 'sim',
              icon: 'check',
            },
            {
              label: 'Não',
              id: 'nao',
              icon: 'close',
            },
          ],
        })
        .onOk((action) => {
          if (action.id === 'sim') {
              this.pk = row.id
            erase(this);
          }
        });
    },
    gravar_storage:function(pk){
      if (SessionStorage.has('animal')){
        SessionStorage.remove('animal')
      }
      SessionStorage.set('animal', pk)
    },
    cadastrar_cliente: function() {
      this.$router.push('/cliente/cadastro');
    },
    cadastrar_animal: function() {
      this.$router.push('/animal/cadastro');
    },
    cadastrar_medicamento: function() {
      this.$router.push('/medicamento/cadastro');
    },
    cadastrar_doenca: function() {
      this.$router.push('/doenca/cadastro');
    },
    buscar_cliente: function() {
      this.$router.push('/cliente/busca');
    },
    registrar_consulta: function(pk) {
      this.gravar_storage(pk)
      this.$router.push(`/consulta/cadastro/${pk}`);
    },
    buscar_consulta: function(pk) {
      this.gravar_storage(pk)
      this.$router.push(`/consulta/busca/${pk}`);
    },
    registrar_cirurgia: function(pk) {
      this.gravar_storage(pk)
      this.$router.push(`/cirurgia/cadastro/${pk}`);
    },
    buscar_cirurgia: function(pk) {
      this.gravar_storage(pk)
      this.$router.push(`/cirurgia/busca/${pk}`);
    },
    registrar_emergencia: function(pk) {
      this.gravar_storage(pk)
      this.$router.push(`/emergencia/cadastro/${pk}`);
    },
    buscar_emergencia: function(pk) {
      this.gravar_storage(pk)
      this.$router.push(`/emergencia/busca/${pk}`);
    },
    registrar_atendimento: function(pk) {
      this.gravar_storage(pk)
      this.$router.push(`/atendimento/cadastro/${pk}`);
    },
    buscar_atendimento: function(pk) {
      this.gravar_storage(pk)
      this.$router.push(`/atendimento/busca/${pk}`);
    },
    registrar_vacina: function(pk) {
      this.gravar_storage(pk)
      this.$router.push(`/vacina/cadastro/${pk}`);
    },
    buscar_vacina: function(pk) {
      this.gravar_storage(pk)
      this.$router.push(`/vacina/busca/${pk}`);
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
    if (this.$route.params.cliente != null) {
      this.cliente = this.$route.params.cliente;
    }
    this.load();
  }
});
</script>

<style>
.row {
  margin: 1px;
}
</style>
