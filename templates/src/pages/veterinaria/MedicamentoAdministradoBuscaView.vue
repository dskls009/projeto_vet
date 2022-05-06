<template>
  <q-page padding class="full-width">
    <div class="column items-end">
      <div class="col">
        <q-btn
          :label="pegar_tipo()"
          flat
          color="negative"
          icon="arrow_back"
          @click="voltar_busca"
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
          title="Medicamentos Administrados"
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
                      `/medicamento_administrado/edicao/${pegar_id(
                        props.row
                      )}/${props.row.id}`
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
              <q-td :props="props" key="relacao">
                {{ pegar_relacao(props.row) }}
              </q-td>
              <q-td :props="props" key="descricao">
                {{ pegar_descricao(props.row) }}
              </q-td>
              <q-td :props="props" key="medicamento__medicamento">
                {{ props.row.medicamento__medicamento }}
              </q-td>
              <q-td :props="props" key="quantidade_administrada">
                {{ props.row.quantidade_administrada }}
              </q-td>
              <q-td :props="props" key="medicamento__unidade_medida">
                {{ props.row.medicamento__unidade_medida }}
              </q-td>
              <q-td :props="props" key="data_aplicacao">
                {{ arrumar_data(props.row.data_aplicacao) }}
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
import { findall, erase } from '../../services/veterinaria/MedicamentoAdministradoService';
import { SessionStorage } from 'quasar';

export default defineComponent({
  name: 'MedicamentoAdministradoBuscaView',
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
      consulta: undefined,
      cirurgia: undefined,
      emergencia: undefined,
      atendimento: undefined,
      columns: [
        {
          name: 'id',
          label: 'Ações',
          align: 'center',
          sortable: false
        },
        {
          name: 'relacao',
          label: 'Relação',
          align: 'left',
          sortable: false
        },
        {
          name: 'descricao',
          label: 'Descrição',
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
          name: 'quantidade_administrada',
          label: 'Quantidade',
          align: 'left',
          sortable: false
        },
        {
          name: 'medicamento__unidade_medida',
          label: 'Unidade de Medida',
          align: 'left',
          sortable: false
        },
        {
          name: 'data_aplicacao',
          label: 'Data de Aplicação',
          align: 'left',
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
    voltar_busca: function() {
      if (this.consulta != null) {
        this.$router.push(
          `/consulta/busca/${SessionStorage.getItem('animal')}`
        );
      } else if (this.cirurgia != null) {
        this.$router.push(
          `/cirurgia/busca/${SessionStorage.getItem('animal')}`
        );
      } else if (this.emergencia != null) {
        this.$router.push(
          `/emergencia/busca/${SessionStorage.getItem('animal')}`
        );
      } else if (this.atendimento != null) {
        this.$router.push(
          `/emergencia/busca/${SessionStorage.getItem('animal')}`
        );
      }
    },
    pegar_tipo: function(){
if (this.consulta != null) {
        return 'Buscar Consulta'
      } else if (this.cirurgia != null) {
        return 'Buscar Cirurgia'
      } else if (this.emergencia != null) {
        return 'Buscar Emergência'
      } else if (this.atendimento != null) {
        return 'Buscar Atendimento'
      }
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
    pegar_relacao: function(row) {
      if (row.consulta__id != null) {
        return 'Consulta';
      } else if (row.cirurgia__id != null) {
        return 'Cirurgia';
      } else if (row.emergencia__id != null) {
        return 'Emergência';
      } else if (row.atendimento__id != null) {
        return 'Atendimento';
      }
    },
    pegar_descricao: function(row) {
      if (row.consulta__id != null) {
        return row.consulta__descricao;
      } else if (row.cirurgia__id != null) {
        return row.cirurgia__descricao;
      } else if (row.emergencia__id != null) {
        return row.emergencia__descricao;
      } else if (row.atendimento__id != null) {
        return row.atendimento__descricao;
      }
    },
    pegar_id: function(row) {
      if (row.consulta__id != null) {
        return 'consulta/' + row.consulta__id;
      } else if (row.cirurgia__id != null) {
        return 'cirurgia/' + row.cirurgia__id;
      } else if (row.emergencia__id != null) {
        return 'emergencia/' + row.emergencia__id;
      } else if (row.atendimento__id != null) {
        return 'atendimento/' + row.atendimento__id;
      }
    },
    arrumar_data: function(datetime) {
      if (datetime != null && datetime != undefined) {
        let datahora = String(datetime).split('T');
        let data = datahora[0].split('-');
        let hora = datahora[1];
        let dh_format = data[2] + '/' + data[1] + '/' + data[0] + ' ' + hora;
        return dh_format;
      } else {
        return '';
      }
    }
  },
  mounted: function() {
    if (this.$route.params.consulta != null) {
      this.consulta = this.$route.params.consulta;
    } else if (this.$route.params.cirurgia != null) {
      this.cirurgia = this.$route.params.cirurgia;
    } else if (this.$route.params.emergencia != null) {
      this.emergencia = this.$route.params.emergencia;
    } else if (this.$route.params.atendimento != null) {
      this.atendimento = this.$route.params.atendimento;
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
