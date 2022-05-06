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
          title="Recetuário"
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
                  @click="$router.push(`/receituario/edicao/${props.row.id}`)"
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
              <q-td :props="props" key="doenca__doenca">
                {{ props.row.doenca__doenca }}
              </q-td>
              <q-td :props="props" key="medicamento__medicamento">
                {{ props.row.medicamento__medicamento }}
              </q-td>
              <q-td :props="props" key="receita">
                {{ props.row.receita }}
              </q-td>
              <q-td :props="props" key="anexo">
                <q-btn
                  size="sm"
                  dense
                  icon="attach_file"
                  flat
                  rounded
                  @click="baixar_anexo(props.row.anexo__id)"
                />
              </q-td>
              <q-td :props="props" key="observacao">
                {{ props.row.observacao }}
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
import { findall, erase } from '../../services/veterinaria/ReceituarioService';
import { download } from './../../services/commons/Base64Service';

export default defineComponent({
  name: 'ReceituarioBuscaView',
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
          name: 'doenca__doenca',
          label: 'Doença',
          align: 'left',
          sortable: false
        },
        {
          name: 'medicamento__medicamento',
          label: 'Medicamento',
          align: 'left',
          sortable: false
        },
        {
          name: 'receita',
          label: 'Receita',
          align: 'left',
          sortable: false
        },
        {
          name: 'anexo',
          label: 'Anexo',
          align: 'center',
          sortable: false
        },
        {
          name: 'observacao',
          label: 'Observação',
          align: 'left',
          sortable: true
        }
      ]
    };
  },
  methods: {
    load: function() {
      findall(this);
    },
    download: function() {
      download(this);
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
    baixar_anexo: function(anexo__id) {
      this.pk = anexo__id;
      this.download();
    }
  },
  mounted: function() {
    this.load();
  }
});
</script>

<style>
.row {
  margin: 1px;
}
</style>
