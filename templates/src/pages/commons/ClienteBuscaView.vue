<template>
  <q-page padding class="full-width">
    <div class="column items-end">
    <div class="col">
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
      >
        <template v-slot:top-right>
          <q-input outlined dense debounce="300" v-model="filtro" @input="load">
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
                @click="$router.push(`/cliente/edicao/${props.row.id}`)"
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
            <q-td :props="props" key="cpf">{{ props.row.cpf }} </q-td>
            <q-td :props="props" key="nome">{{ props.row.nome }} </q-td>
            <q-td :props="props" key="sobrenome"
              >{{ props.row.sobrenome }}
            </q-td>
            <q-td :props="props" key="email">{{ props.row.email }} </q-td>
            <q-td :props="props" key="telefone_1"
              >{{ props.row.telefone_1 }}
            </q-td>
            <q-td :props="props" key="telefone_2"
              >{{ props.row.telefone_2 }}
            </q-td>
            <q-td :props="props" key="animais">
              <q-btn
                size="sm"
                dense
                icon="search"
                flat
                color="primary"
                rounded
                @click="buscar_animal(props.row.id)"
              />
              <q-btn
                size="sm"
                dense
                icon="add"
                flat
                color="primary"
                rounded
                @click="cadastrar_animal(props.row.id)"
              />
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
import { findall, erase } from '../../services/commons/ClienteService';
import { SessionStorage } from 'quasar';

export default defineComponent({
  name: 'ClienteBuscaView',
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
          name: 'animais',
          label: 'Animais',
          align: 'center',
          sortable: false
        }
      ]
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
    gravar_storage: function(pk){
      if (SessionStorage.has('cliente')){
        SessionStorage.remove('cliente')
      }
      SessionStorage.set('cliente', pk)
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
    buscar_animal: function(pk){
      this.gravar_storage(pk)
      this.$router.push(`/animal/busca/${pk}`)
    },
    cadastrar_animal: function(pk){
      this.gravar_storage(pk)
      this.$router.push(`/animal/cadastro/${pk}`)
    }
  },
  mounted: function() {
    this.load();
  }
});
</script>

<style>
  .row{
    margin: 1px;
  }
</style>
