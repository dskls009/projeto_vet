<template>
  <q-page padding class="full-width">
    <div class="column items-end">
      <div class="col">
        <q-btn
          label="Buscar Animal"
          flat
          color="negative"
          icon="arrow_back"
          @click="buscar_animal"
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
          title="Consultas"
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
                  @click="
                    $router.push(
                      `/consulta/edicao/${props.row.animal__id}/${props.row.id}`
                    )
                  "/>
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
              <q-td :props="props" key="animal__cliente__cpf">
                {{ props.row.animal__cliente__cpf }}
              </q-td>
              <q-td :props="props" key="animal__rga">
                {{ props.row.animal__rga }}
              </q-td>
              <q-td :props="props" key="animal__nome">
                {{ props.row.animal__nome }}
              </q-td>
              <q-td :props="props" key="descricao">
                {{ props.row.descricao }}
              </q-td>
              <q-td :props="props" key="datahora_inicio">
                {{ arrumar_data(props.row.datahora_inicio) }}
              </q-td>
              <q-td :props="props" key="datahora_fim">
                {{ arrumar_data(props.row.datahora_fim) }}
              </q-td>
              <q-td :props="props" key="observacao">
                {{ props.row.observacao }}
              </q-td>
              <q-td :props="props" key="medicamento">
                <q-btn
                  size="sm"
                  dense
                  icon="search"
                  flat
                  color="primary"
                  rounded
                  @click="buscar_medicamento(props.row.id)"
                />
                <q-btn
                  size="sm"
                  dense
                  icon="add"
                  flat
                  color="primary"
                  rounded
                  @click="registrar_medicamento(props.row.id)"
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
import { findall, erase } from '../../services/veterinaria/ConsultaService';
import { SessionStorage } from 'quasar';

export default defineComponent({
  name: 'ConsultaBuscaView',
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
      animal: undefined,
      columns: [
        {
          name: 'id',
          label: 'Ações',
          align: 'center',
          sortable: false
        },
        {
          name: 'animal__cliente__cpf',
          label: 'Tutor CPF',
          align: 'left',
          sortable: false
        },
        {
          name: 'animal__rga',
          label: 'Animal RGA',
          align: 'left',
          sortable: false
        },
        {
          name: 'animal__nome',
          label: 'Animal Nome',
          align: 'left',
          sortable: false
        },
        {
          name: 'descricao',
          label: 'Descrição',
          align: 'left',
          sortable: true
        },
        {
          name: 'datahora_inicio',
          label: 'Início',
          align: 'left',
          sortable: true
        },
        {
          name: 'datahora_fim',
          label: 'Término',
          align: 'left',
          sortable: true
        },
        {
          name: 'observacao',
          label: 'Observação',
          align: 'left',
          sortable: true
        },
        {
          name: 'medicamento',
          label: 'Medicamento',
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
    buscar_animal: function() {
      if (SessionStorage.has('cliente')){
        this.$router.push(`/animal/busca/${SessionStorage.getItem('cliente')}`);
      } else {
        this.$router.push('/animal/busca');
      }
    },
    registrar_medicamento: function(pk) {
      this.$router.push(`/medicamento_administrado/cadastro/consulta/${pk}`);
    },
    buscar_medicamento: function(pk) {
      this.$router.push(`/medicamento_administrado/busca/consulta/${pk}`);
    },
    arrumar_data: function(datetime){
      if (datetime != null && datetime != undefined){
        let datahora = String(datetime).split('T')
        let data = datahora[0].split('-')
        let hora = datahora[1]
        let dh_format = data[2]+'/'+data[1]+'/'+data[0]+' '+hora
        return dh_format
      } else {
        return ''
      }
    }
  },
  mounted: function() {
    if (this.$route.params.animal != null) {
      this.animal = this.$route.params.animal;
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
